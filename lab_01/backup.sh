PATH_TO_FILE=$1
DEST_TO_SAVE=${2:-/c/backup}

if [ -z "$PATH_TO_FILE" ]; then
    echo "введите директорию для резервного копирования"
    exit 1
fi

if [ ! -d "$PATH_TO_FILE" ]; then
    echo "директория '$PATH_TO_FILE' не существует."
    exit 1
fi

if [ ! -d "$DEST_TO_SAVE" ]; then
    echo "директория для создания копии '$DEST_TO_SAVE' не ссуществует, создаем..."
    mkdir -p "$DEST_TO_SAVE"
fi

DATE=$(date +%m-%d_%H-%M)
BASENAME=$(basename "$PATH_TO_FILE")
ARCHIVE_NAME="${DEST_TO_SAVE}/${BASENAME}_${DATE}.tar.gz"

tar -czf "$ARCHIVE_NAME" -C "$(dirname "$PATH_TO_FILE")" "$BASENAME"

echo "резервная копия создана в: $ARCHIVE_NAME"

echo "содержимое папки: '$DEST_TO_SAVE'" 
cd "$DEST_TO_SAVE"
ls
