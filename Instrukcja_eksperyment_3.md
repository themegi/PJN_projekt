# Instrukcja do wykonania 3 eksperymentu z projektu przetwarzania języka natrualnego
Ze względu na to, że samo wykonanie tego eksperymentu nie wymagało tworzenia skryptów ani pisania kodu przygotowana została instrukcja jak zaimpelementować to samo środowisko jakie był użyte.

## Opis eksperymentu
Badanie zostanie przeprowadzone lokalnie, z wykorzystaniem kilku modeli (Mistral 3, Gemma3:12b, Gemma3:4b i innych) które będą sprawnie działać na systemie z 12 Gb pamięci VRAM, uruchamianych za pomocą Ollamy i OpenUI do ułatwienia pracy oraz zbioru danych CNN/Daily Mail. W pierwszym etapie przygotowana zostanie próbka 10 wybranych artykułów z obu zbiorów. Następnie zostaną opracowane różne wersje promptów, w których w odmienny sposób zostanie sformułowane polecenie dotyczące długości streszczenia; w prompcie zawsze będzie podana żądana długość streszczenia w zdaniach. Dla każdego artykułu i każdego wariantu promptu każdy z modeli wygeneruje streszczenie, a następnie zostanie zmierzona ich długość. W dalszej części eksperymentu przeprowadzona zostanie analiza wyników polegająca na obliczeniu średniej, odchylenia standardowego i przeciętnego odchylenia od założonej długości streszczenia dla każdej kombinacji promptu i modelu.
### Pytanie badawcze
Ten eksperyment stara się odpowiedzieć na pytanie:
*Jak sposób sformułowania promptu wpływa na dokładność długości streszczenia*
generowanego przez duży model językowy (LLM)?
## Implementacja środowiska
Całe środowisko zostało zainstalowane na maszynie wirtualnej z systemu Linux. 
### Instalacja Ollama
**Ollama** to lokalny serwer do uruchamiania modeli językowych na własnym komputerze, pozwala również pobierać opublikowane modele z chmury.
#### Pobranie i uruchomienie skryptu instalacji
```
curl -fsSL https://ollama.com/install.sh | sh
```
#### Weryfikacja instalacji przez pobranie modelu
```
ollama run llama3
```
### Instalacja Open WebUI
**Open WebUI** to graficzny interfejs do Ollama, umożliwiający wygodne korzystanie z lokalnych modeli językowych przez przeglądarkę.
#### Instalacja Docker
Open WebUI będzie zainstalowane jako kontener programu Docker, więc na początku należy zainstalować Dockera.
```
sudo apt install docker.io -y
sudo usermod -aG docker $USER
newgrp docker 
```
#### Konfiguracja Open WebUI
```
docker run -d --network=host \
  --name open-webui \
  -v open-webui:/app/backend/data \
  -e OLLAMA_BASE_URL=http://127.0.0.1:11434 \
  --restart unless-stopped \
  ghcr.io/open-webui/open-webui:main
```
To spowoduje, że UI będzie dostępne pod adresem http://localhost:8080.
#### Weryfikacja i pierwsze logowanie do Open WebUI
Ollama, Docker i kontener OpenUI muszą działać, wtedy należy wejść na adres http://localhost:8080. Jeśli pojawi się ekran logowania oznacza to, że instalacja zakończyła się poprawnie. Należy stworzyć nowe konto i zalogować się aby mieć dostęp do zainstalowanych modeli.
### Konfiguracja środowiska
Po otwarciu okna nowego czatu w prawym górnym rogu widoczne są trzy kropki. Po kliknięciu ich możwlie jest wpisanie system promptu do tego chatu. Oznacza to, że do każdej wiadomości wysłanej w tym oknie, na początku zostanie dodany system prompt. W taki sposób można testować prompty opisane w pracy.



