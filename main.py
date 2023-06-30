import os
import chess.pgn
from PIL import Image

piece_colors = {True: "w", False: "b"}

piece_names = {1: "p", 2: "n", 3: "b", 4: "r", 5: "q", 6: "k"}


def generate_gifs(
    pgn_file, output_folder, frame_duration=800, last_frame_duration=3000
):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    board_image = Image.open("assets/board.png").convert("RGBA")

    piece_images = {}
    for color in ["w", "b"]:
        for piece_name in ["k", "q", "r", "b", "n", "p"]:
            piece_image = Image.open(f"assets/{color}{piece_name}.png").convert("RGBA")
            piece_images[f"{color}{piece_name}"] = piece_image

    pgn = open(pgn_file)
    game_number = 1

    while True:
        game = chess.pgn.read_game(pgn)
        if game is None:
            break

        board_positions = []
        board = game.board()
        board_positions.append(board.copy())
        for move in game.mainline_moves():
            board.push(move)
            board_positions.append(board.copy())

        gif_frames = []
        for i, position in enumerate(board_positions):
            frame = board_image.copy()
            for square, piece in position.piece_map().items():
                if piece.piece_type != chess.PieceType(0):
                    piece_image = piece_images[
                        f"{piece_colors[piece.color]}{piece_names[piece.piece_type]}"
                    ]
                    x = (square % 8) * 177
                    y = (7 - square // 8) * 177
                    frame.paste(piece_image, (x, y), piece_image)
            gif_frames.append(frame)

            if i == len(board_positions) - 1:
                gif_frames[-1].info["duration"] = last_frame_duration
            else:
                gif_frames[-1].info["duration"] = frame_duration

        output_file = os.path.join(output_folder, f"game{game_number}.gif")
        gif_frames[0].save(
            output_file,
            format="GIF",
            append_images=gif_frames[1:],
            save_all=True,
            loop=0,
        )

        print(f"GIF file {output_file} generated successfully.")
        game_number += 1


# Example
if __name__ == "__main__":
    pgn_file = "game.pgn"
    output_folder = "output"
    generate_gifs(pgn_file, output_folder)
