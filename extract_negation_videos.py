import pandas as pd
import pympi
import ffmpeg

def cut_fragment(row):
    eaf_path = row['TranscriptionPath']
    eaf = pympi.Elan.Eaf(eaf_path)
    linked = eaf.get_linked_files()

    if 'RELATIVE_MEDIA_URL' in linked[0]:
        mp4_info = linked[0]['RELATIVE_MEDIA_URL']
        mp4_name = "./Корпус/" + mp4_info.split('/')[-1]
        print('Extracting fragment ', index, ' in file ', mp4_name)

        start = row['AnnotationBeginTime']
        end = row['AnnotationEndTime']

        cut_name = './extracted negation/' + filename.strip('.csv') + '_' + str(index) + '.mp4'

        try:
            (
                ffmpeg
                    .input(mp4_name)
                    .trim(start=start / 1000.0, end=end / 1000.0)
                    .setpts('PTS-STARTPTS')
                    .output(cut_name)
                    .run(capture_stdout=True, capture_stderr=True)
            )
        except ffmpeg.Error as e:
            print('stdout:', e.stdout.decode('utf8'))
            print('stderr:', e.stderr.decode('utf8'))
            raise e


def process_one_file(filename: str):
    with open(filename, encoding='utf-8') as f:
        df = pd.read_csv(f, sep=';')
        df.drop(df.index[[0]], inplace=True)
        df.drop_duplicates(subset=['AnnotationBeginTime', 'AnnotationEndTime', 'TranscriptionPath'],
                           inplace=True,
                           ignore_index=True)

    df.apply(lambda x: cut_fragment(x), axis=1)




def main():
    for i in range(6):
        print('Processing file '+ str(i+1))
        process_one_file(f'Поиск {i+1}.csv')


if __name__ == '__main__':
    main()

