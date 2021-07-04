import argparse

PORT = 1337

def  main(args):
  input_filename = args.i
  output_filename = args.o
  with open(input_filename, 'r') as myfile:
    content = myfile.readlines()

  urls = []
  for line in content:
    url = line.strip()
    urls.append("\""+ url + "\"")

  web_var = "websites = ["+ ", ".join(urls) +"]"

  build_html = ["""
  <!DOCTYPE html>
  <html lang="de">
  <head>
    <title>Internet-Safari</title>
    <style>
    body {
      background-color: #333;
      color: white;
    }
    a:visited {
      color: #CCC;
    }
    a, a:hover {
      color: white;
    }
    iframe {
      width: 100%;
      min-height: 600px;
    }
    button {
      padding: 20px;
    }
    #menue {
      margin-bottom: 10px;
    }
    </style>
    <script>
    timer = undefined
    """+ web_var +"""
    current = parseInt(localStorage.getItem("current")) || 0
    if (websites.length - 1 < parseInt(current)) {
      current = 0
    }
    
    function next() {
      clearTimeout(timer)
      document.querySelector("#frame").setAttribute("src", "about:blank")
      current++
      localStorage.setItem("current", current)
      document.querySelector("#url").setAttribute("href", websites[current])
      document.querySelector("#url").innerText = websites[current]
      document.querySelector("#frame").setAttribute("src", websites[current])
      document.querySelector("#stat").innerText = current + " of " + (websites.length - 1) + " Websites"
      timer = setTimeout(next, 5 * 1000)
    }
    function stop() {
      clearTimeout(timer)
    }
    function back() {
      clearTimeout(timer)
      document.querySelector("#frame").setAttribute("src", "about:blank")
      current--
      localStorage.setItem("current", current)
      document.querySelector("#url").setAttribute("href", websites[current])
      document.querySelector("#url").innerText = websites[current]
      document.querySelector("#frame").setAttribute("src", websites[current])
      document.querySelector("#stat").innerText = current + " of " + (websites.length - 1) + " Websites"
      timer = setTimeout(next, 5 * 1000)
    }
    </script>
  </head>
  <body>
  <div id="menue">
    <button onclick="back()">Back</button> <button onclick="stop()">Stop autoload</button> 
    <button onclick="next()">Next</button> URL: <a id="url" href="" target="_blank"></a>, <span id="stat"></span>, 
    <a href="#" onclick="current=0;next();back()">Back to start.</a>
  </div>
  <div id="main">
    <iframe id="frame" referrerpolicy="no-referrer" sandbox="allow-scripts, allow-forms"></iframe>
  </div>
  <script>
    next()
    back()
  </script>
  </body>
  </html>
  """]

  full_html = "\n".join(build_html)
  with open(output_filename, 'w') as myfile:
    myfile.write(full_html)

  print("File generated!")

if __name__ == "__main__":
  parser = argparse.ArgumentParser(description='Generate a html file to slide through website urls')
  parser.add_argument('-i', type=str, default="./input.txt", help='Path to input file')
  parser.add_argument('-o', type=str, default="./output.html", help='Path to output file')
  args = parser.parse_args()
  main(args)
