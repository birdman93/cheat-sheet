import whisper


models = {
        1: 'tiny',
        2: 'base',
        3: 'small',
        4: 'medium',
        5: 'large'
    }


def speech_recognition(model='base'):

    speech_model = whisper.load_model(model)
    result = speech_model.transcribe(audio="D:\\Coding\\Python Experiments\\SpeechToText\\track.mp3", fp16=False)

    with open(f"transcription_{model}.txt", 'w', encoding='utf-8') as file:
        print(result)
        file.write(result['text'])


def main():

    for key, value in models.items():
        print(f"{key}: {value}")

    model = int(input('\nВыберете модель, передав цифру от 1 до 5: '))

    if model not in models.keys():
        raise KeyError('Такого значения нет')

    print('\nПроцесс запущен...\n')
    speech_recognition(model=models[model])


if __name__ == '__main__':
    main()
