<div align="center">
  <h1>Lai-K API</h1>
  <img src="./assets/images/logo.png" alt="drawing" width="200"/>
  <p>Flask Back-end para Lai-K</p>
</div>

## Installation

Windows (PowerShell)
<pre><code>
[Environment]::SetEnvironmentVariable('DB_URI', {uri})
</code></pre>
Linux & Mac
<pre><code>
echo "export DB_URI={uri}" >> ~/.profile
</code></pre>
Restart shell and execute
<pre><code>
git clone https://github.com/moonsh4ke/lai-k-api
</code></pre>
<pre><code>
cd lai-k-api
</code></pre>
<pre><code>
pip install virtualenv
</code></pre>
<pre><code>
virtualenv env
</code></pre>
Windows (PowerShell)
<pre><code>
.\env\Scripts\activate
</code></pre>
Linux & Mac
<pre><code>
source ./env/bin/Activate
</code></pre>
<pre><code>
pip install -r requirements.txt
</code></pre>
<pre><code>
python app.py
</code></pre>
