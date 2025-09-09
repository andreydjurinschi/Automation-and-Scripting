PATH_TO_FILE=$1
DEST_TO_SAVE=${2:-backup}   
if [ -z "$PATH_TO_FILE" ]; then
    echo "введите директорию для резервного копирования"
    exit 1
fi

if [ ! -d "$PATH_TO_FILE" ]; then
    echo "директория '$PATH_TO_FILE' не существует."
    exit 1
fi


DEST_ON_C="/c/$DEST_TO_SAVE"

if [ ! -d "$DEST_ON_C" ]; then
    echo "директория '$DEST_ON_C' не существует, создаем..."
    mkdir -p "$DEST_ON_C"
fi

DATE=$(date +%m-%d_%H-%M)
BASENAME=$(basename "$PATH_TO_FILE")

tar -czf "${DEST_ON_C}/${BASENAME}_${DATE}.tar.gz" -C "$(dirname "$PATH_TO_FILE")" "$BASENAME"

echo "резервная копия создана в: "${DEST_ON_C}/${BASENAME}_${DATE}.tar.gz""

echo "содержимое папки '$DEST_ON_C':"
ls "$DEST_ON_C"
