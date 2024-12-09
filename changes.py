
import os
from pytubefix import YouTube
from tqdm import tqdm
from tkinter import Tk, filedialog
import subprocess

def escolher_diretorio():
    root = Tk()
    root.withdraw()  
    pasta = filedialog.askdirectory(title="Escolha o diretório para salvar o vídeo")
    return pasta

def baixar_video(url, caminho_salvar, resolucao_escolhida):
    try:
        yt = YouTube(url)
        video_stream = yt.streams.filter(file_extension="mp4", resolution=resolucao_escolhida).first()
        if not video_stream:
            print(f"Resolução {resolucao_escolhida} não disponível. Baixando na melhor resolução disponível.")
            video_stream = yt.streams.filter(file_extension="mp4").order_by('resolution').desc().first()
        audio_stream = yt.streams.filter(only_audio=True).first()

        if not video_stream or not audio_stream:
            print("Erro ao encontrar o stream de vídeo ou áudio.")
            return

        print(f"Iniciando o download de: {yt.title}")
        print(f"Resolução do vídeo: {video_stream.resolution}")

        video_path = os.path.join(caminho_salvar, f"{yt.title}_video.mp4")
        audio_path = os.path.join(caminho_salvar, f"{yt.title}_audio.mp3")
        
        video_stream.download(output_path=caminho_salvar, filename=f"{yt.title}_video.mp4")
        audio_stream.download(output_path=caminho_salvar, filename=f"{yt.title}_audio.mp3")

        output_path = os.path.join(caminho_salvar, f"{yt.title}_final.mp4")

        subprocess.run(['ffmpeg', '-i', video_path, '-i', audio_path, '-c:v', 'copy', '-c:a', 'aac', output_path], check=True)

        print("Download e mesclagem concluídos!")
        os.remove(video_path)
        os.remove(audio_path)

    except Exception as e:
        print(f"Erro ao baixar o vídeo: {e}")

def main():
    url = input("Cole o link do vídeo do YouTube: ")
    resolucao_escolhida = input("Escolha a resolução (exemplo: 2160p, 1080p, 720p): ")
    pasta = escolher_diretorio()
    if pasta:
        baixar_video(url, pasta, resolucao_escolhida)
    else:
        print("Nenhuma pasta foi selecionada. O download não pode continuar.")

if __name__ == "__main__":
    main()
