
import librosa
import librosa.display

def mfccfn(audio_file):
# Load an audio file
#     audio_file = 'recording13029.wav_norm_mono.wav'

    # Load the audio file using librosa
    y, sr = librosa.load(audio_file)

    # Calculate MFCCs
    mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
    print(mfccs.shape)

    f=[]
    for i in range(13):
        r=[]
        for j in range(60):
            r.append(mfccs[i][j])
        f.append(r)


    return f

