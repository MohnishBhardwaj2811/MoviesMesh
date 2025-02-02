from flask import Flask, request, render_template_string ,jsonify
import re
from bs4 import BeautifulSoup
import requests
import base64


######33######################################################################################################################################################################################
######33######################################################################################################################################################################################
######33######################################################################################################################################################################################
######33######################################################################################################################################################################################
######33######################################################################################################################################################################################
######33######################################################################################################################################################################################
######33######################################################################################################################################################################################
######33######################################################################################################################################################################################

def Convert_magnet_torrent(magnet_url):
    magnet_url = magnet_url.replace("1CBE3A5D27F112A53C54EDCA8EA674BBB7D07FDE", "1cbe3a5d27f112a53c54edca8ea674bbb7d07fde")
    base64_magnet = base64.b64encode(magnet_url.encode()).decode()
    utorrent_url = f"https://lite.utorrent.com/player?m={base64_magnet}"  #f"/player/{base64_magnet}"
    return utorrent_url
    
def extract_search(url):

    html_content = requests.get(url).text
    soup = BeautifulSoup(html_content, 'html.parser')
    results = []# Find all table rows containing torrent entries
    for row in soup.select('td.vertTh + td'):
        # Extract movie name
        name_tag = row.select_one('a.detLink')
        movie_name = name_tag.text.strip() if name_tag else None

        # Extract magnet link
        magnet_tag = row.select_one('a[href^="magnet:?"]')
        magnet_link = magnet_tag['href'] if magnet_tag else None

        # Extract upload date and size
        det_desc = row.select_one('font.detDesc')
        if det_desc:
            text = det_desc.get_text(strip=True)
            
            # Extract uploaded date
            uploaded_match = re.search(r'Uploaded (.*?),', text)
            uploaded = uploaded_match.group(1).replace('\xa0', ' ') if uploaded_match else None
            
            # Extract size
            size_match = re.search(r'Size (.*?),', text)
            size = size_match.group(1).replace('\xa0', ' ') if size_match else None
        else:
            uploaded = size = None

        results.append({
            'movie_name': movie_name,
            'magnet_link': Convert_magnet_torrent(magnet_link),
            'uploaded': uploaded,
            'size': size
        })
    
    return results


######33######################################################################################################################################################################################
######33######################################################################################################################################################################################
######33######################################################################################################################################################################################
######33######################################################################################################################################################################################
######33######################################################################################################################################################################################
######33######################################################################################################################################################################################
######33######################################################################################################################################################################################
######33######################################################################################################################################################################################


html_content1 = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MoviesMesh - Search and Stream</title>
    <style>
        /* Hidden by default */
        .embed-container {
            display: none;
            width: 1280px;
            height: 600px;
            overflow: hidden;
            position: relative;
            margin: 20px auto;
            border: 2px solid #333;
            border-radius: 8px;
            scale: 0.6;
        }

        .embed-container.active {
            display: block;
        }

        .embed-container iframe {
            position: relative;
            width: 2000px;
            height: 1090px;
            top: -240px;
            left: -360px;
            
            border: none;
            scale: 1;
        }

        .movie-link {
            color: black;
            text-decoration: none;
            cursor: pointer;
        }

        body {
            font-family: 'Arial', sans-serif;
            margin: 0;
            padding: 0;
            background-color: #f4f4f4;
            color: #333;
        }

        .container {
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            padding: 20px;
            flex-direction: column;
        }

        .search-box {
            background-color: #fff;
            padding: 40px;
            border-radius: 8px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            text-align: center;
            width: 100%;
            max-width: 600px;
            margin-bottom: 20px;
        }

        .search-box h1 {
            font-size: 24px;
            margin-bottom: 20px;
        }

        .search-box input {
            padding: 10px;
            font-size: 16px;
            width: 80%;
            margin-bottom: 20px;
            border: 2px solid #ddd;
            border-radius: 4px;
            outline: none;
        }

        .search-box button {
            padding: 10px 20px;
            font-size: 16px;
            background-color: #007BFF;
            color: #fff;
            border: none;
            border-radius: 4px;
            cursor: pointer;
        }

        .search-box button:hover {
            background-color: #0056b3;
        }

        .movie-list {
            text-align: left;
            font-size: 16px;
            margin-top: 20px;
        }

        .movie-list ul {
            list-style-type: none;
            padding: 0;
        }

        .movie-list li {
            padding: 15px 0;
            border-bottom: 1px solid #ddd;
        }

        .back-btn {
            display: inline-block;
            padding: 10px 20px;
            background-color: #28a745;
            color: #fff;
            text-decoration: none;
            border-radius: 4px;
            font-size: 16px;
            margin-top: 20px;
        }
    </style>
</head>
<body>
    <div class="container">
        <!-- Search Form -->
        <div class="search-box">
            <h1>MoviesMesh</h1>
            <p>One Site For All Entertainment!</p>
            <form action="/" method="get">
                <input type="text" name="query" placeholder="Enter movie name...">
                <button type="submit">Search</button>
            </form>
        </div>

        <!-- Video Player (hidden initially) -->
        <div class="embed-container" id="playerContainer">
            <iframe id="videoPlayer" src="" 
                    scrolling="no"
                    allow="autoplay; encrypted-media"
                    sandbox="allow-same-origin allow-scripts allow-forms">
            </iframe>
            
        </div>

        <button id="fullscreenButton">Go Fullscreen</button>

        <!-- Search Results -->
        {% if query %}
        <div class="search-box">
            {% if movies %}
            <div class="movie-list">
                <ul>
                    {% for movie in movies %}
                    <li>
                        <a href="#" class="movie-link" 
                           onclick="playMovie('{{ movie.magnet_link }}')">
                            {{ movie.movie_name }}
                        </a>
                        <div class="meta">
                            <small>Uploaded: {{ movie.uploaded }}</small>
                            <small>Size: {{ movie.size }}</small>
                        </div>
                    </li>
                    {% endfor %}
                </ul>
            </div>
            {% else %}
            <p>No results found for "{{ query }}"</p>
            {% endif %}
            <a href="/" class="back-btn">New Search</a>
        </div>
        {% endif %}
    </div>

     <script>

             // New Fullscreen functionality with scaling control
        const fullscreenButton = document.getElementById('fullscreenButton');
        const playerContainer = document.getElementById('playerContainer');
        let isFullscreen = false;
        let originalTransform = '';

        function calculateScale() {
            const containerWidth = 1280;  // Original width
            const containerHeight = 710;  // Original height
            
            const widthScale = window.innerWidth / containerWidth;
            const heightScale = window.innerHeight / containerHeight;
            
            // Use the smaller scale to maintain aspect ratio
            return Math.min(widthScale, heightScale) * 0.95;  // 95% of max scale to add some padding
        }

        function toggleFullscreen() {
            if (!isFullscreen) {
                // Enter fullscreen
                originalTransform = playerContainer.style.transform;
                playerContainer.style.transform = `scale(${calculateScale()})`;
                playerContainer.style.margin = '0 auto';
                document.documentElement.style.overflow = 'hidden';
                
                if (playerContainer.requestFullscreen) {
                    playerContainer.requestFullscreen();
                }
                isFullscreen = true;
                
                // Add resize listener for window resizing
                window.addEventListener('resize', handleFullscreenResize);
            } else {
                // Exit fullscreen
                playerContainer.style.transform = 'scale(0.6)';
                playerContainer.style.margin = '20px auto';
                document.documentElement.style.overflow = '';
                
                if (document.exitFullscreen) {
                    document.exitFullscreen();
                }
                isFullscreen = false;
                
                // Remove resize listener
                window.removeEventListener('resize', handleFullscreenResize);
            }
        }

        function handleFullscreenResize() {
            if (isFullscreen) {
                playerContainer.style.transform = `scale(${calculateScale()})`;
            }
        }

        // Handle fullscreen changes
        document.addEventListener('fullscreenchange', (e) => {
            if (!document.fullscreenElement && isFullscreen) {
                toggleFullscreen();  // Force exit if user presses ESC
            }
        });

        // Event listeners
        fullscreenButton.addEventListener('click', toggleFullscreen);

        // Keyboard shortcut (F key)
        document.addEventListener('keydown', (e) => {
            if (e.key === 'f' || e.key === 'F') {
                toggleFullscreen();
                e.preventDefault();
            }
        });

        // Modified playMovie function
        function playMovie(magnetLink) {
            const playerContainer = document.getElementById('playerContainer');
            const videoPlayer = document.getElementById('videoPlayer');
            
            // Reset scaling before showing new content
            playerContainer.style.transform = 'scale(0.6)';
            videoPlayer.src = magnetLink;
            playerContainer.classList.add('active');
            playerContainer.scrollIntoView({ behavior: 'smooth' });
            return false;
        }

        // Function to play movie (using magnet link)
        function playMovie(magnetLink) {
            const playerContainer = document.getElementById('playerContainer');
            const videoPlayer = document.getElementById('videoPlayer');
            
            // Convert magnet link to stream URL (example service)
            const streamUrl = magnetLink;
            
            // Update iframe source with the stream URL
            videoPlayer.src = streamUrl;
            
            // Show player container
            playerContainer.classList.add('active');
            
            // Scroll to player
            playerContainer.scrollIntoView({ behavior: 'smooth' });
            
            // Prevent default link behavior (if used in a link)
            return false;
        }
    </script>
</body>
</html>


"""

#####33######################################################################################################################################################################################
######33######################################################################################################################################################################################
######33######################################################################################################################################################################################
######33######################################################################################################################################################################################
######33######################################################################################################################################################################################
######33######################################################################################################################################################################################
######33######################################################################################################################################################################################
######33######################################################################################################################################################################################

app = Flask(__name__)

@app.route('/')
def index():
    query = request.args.get('query', '').replace(" ","%20")
    if query != "":
        search_url =" https://tpirbay.xyz/search/" + query +"/1/99/200"
        movies_data = extract_search(search_url)
        return render_template_string(html_content1, query=query, movies=movies_data)

    # HTML content for both index (search form) and result (query display)
    

    # Render HTML content based on the presence of query
    return render_template_string(html_content1, query=query)

@app.route('/player/<url_id>')
def embededplayer(url_id):
    url = "https://lite.utorrent.com/player?m=" + url_id
    return render_template_string(VideoPlayer(url))

@app.route('/api/<user_id>/<Data_Call>')
def API(user_id,Data_Call):
    id_call = "PLO78H5R7H8O09"
    if user_id == id_call:
        Data_Call = Data_Call.replace(" ","%20")
        Data_Call = " https://tpirbay.xyz/search/" + Data_Call +"/1/99/200"
        data = extract_search(Data_Call)
        return jsonify(data)

#####33######################################################################################################################################################################################
######33######################################################################################################################################################################################
######33######################################################################################################################################################################################
######33######################################################################################################################################################################################
######33######################################################################################################################################################################################
######33######################################################################################################################################################################################
######33######################################################################################################################################################################################
######33######################################################################################################################################################################################



if __name__ == "__main__":
    app.run(debug=True)



