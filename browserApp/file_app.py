import browserApp.model.file as file_model
import browserApp.app as myapp


def start_app():

    model = file_model.FileItem("/Volumes/Orange/GGhost")

    myapp.show_app(model)


if __name__ == "__main__":
    start_app()