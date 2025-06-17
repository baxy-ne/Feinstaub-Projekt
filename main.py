from src.gui.gui import main
from src.core.database import init_db

if __name__ == "__main__":
    init_db()
    main()  