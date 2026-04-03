import argparse


def main():

    parser = argparse.ArgumentParser(
        description="yt-vsc - A yt-dlp based Youtube Downloader"
    )

    parser.add_argument(
        "input",
        default=True,
        help="The youtube link"
     )

    parser.add_argument(
        "-a", "--album",
        action="store_true",
        default=False,
        required=False,
        help="The Album name. Dictate the name of the destination directory."

     )

    parser.add_argument(
        "-m", "--mode",
        default=True,
        required=True,
        help="The download mode. Decides if you want <audio>, <video>, or <both>"
    )
    args = parser.parse_args()

    from ytc import input_check

    if input_check(args.input):

        print(f"[URL Check] Youtube URL confirmed. Proceeding to download.")
        from ytc import download
        download(
            link=args.input,
            isWhat=args.mode,
            isAlbum=args.album
        )
    else:
        print(f"[URL Check] Invalid URL, program terminated.")
        exit(1)
    
if __name__ == "__main__":
    main()