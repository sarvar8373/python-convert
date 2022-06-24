import PyPDF4
from gtts import gTTS
from appJar import gui
from pathlib import Path


def pdf_to_audio(input_file, output_file):
    pdfFileObj = open(input_file, "rb")
    pdfReader = PyPDF4.PdfFileReader(pdfFileObj)

    mytext = ""

    for pageNum in range(pdfReader.numPages):
        pageObj = pdfReader.getPage(pageNum)

        mytext += pageObj.extractText()
    pdfFileObj.close()

    tts = gTTS(text=mytext, lang='en')
    save = str(output_file) + ".mp3"
    tts.save(save)
    if (app.questionBox("Сохранить файл", "Вы хотите выйти из программы?")):
        app.stop()


def validate_inputs(src_file, dest_dir, out_file):
    errors = False
    error_msgs = []
    if (Path(src_file).suffix.upper() != ".PDF"):
        errors = True
        error_msgs.append("Пожалуйста, выберите файл pdf")

    if not (Path(dest_dir)).exists():
        errors = True
        error_msgs.append("Пожалуйста, выберите файл правильно")

    # Check for a file name
    if len(out_file) < 1:
        errors = True
        error_msgs.append("Пожалуйста, введите имя файла")

    return (errors, error_msgs)


def press(button):
    if button == "Process":
        src_file = app.getEntry("Input_File")
        dest_dir = app.getEntry("Output_Directory")
        out_file = app.getEntry("Output_name")
        errors, error_msg = validate_inputs(src_file, dest_dir, out_file)
        if errors:
            app.errorBox("Error", "\n".join(error_msg), parent=None)
        else:
            pdf_to_audio(src_file, Path(dest_dir, out_file))
    else:
        app.stop()


app = gui("Конвертатция PDF в AUDIO", useTtk=True)
app.setTtkTheme('alt')
app.setSize(500, 200)
app.setIcon('images.ico')

# Add the interactive components
app.addLabel("Выберите файл PDF")
app.addFileEntry("Input_File")

app.addLabel("Выберите файл, который хотите сохранить")
app.addDirectoryEntry("Output_Directory")

app.addLabel("Назовите файл")
app.addEntry("Output_name")

app.addButtons(["Process", "Quit"], press)
app.go()
