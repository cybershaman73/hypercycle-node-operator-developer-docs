> For the complete documentation index, see [llms.txt](https://hypercycle-cbno.gitbook.io/hypercycle-cbno/u57KauJomd55OVuTYz6e/llms.txt). Markdown versions of documentation pages are available by appending `.md` to page URLs; this page is available as [Markdown](https://hypercycle-cbno.gitbook.io/hypercycle-cbno/u57KauJomd55OVuTYz6e/hypercycle-aim-deployment/deploy-litellm-aim-w-ui-and-usdc-payments.md).

# Deploy Litellm AIM w/UI & USDC Payments

Compatibility: Can be run on AMD64 & ARM64 architectures and HyperAI Boxes.

Here we deploy our Litellm AIM along with an <mark style="color:$success;">ETH/USDC</mark> payment accepting chat box UI. GPU is not needed for this exercise. Can be deployed on HyperAI Boxes.&#x20;

* Litellm-aim is wrapper that lets us serve and access popular LLMs like ChatGPT, Groq and Google via their API keys.
* In addition to the AIM, we'll be setting up a separate local instance of a web-UI responsible for wallet connect, payment deposit, and an easy to use familiar chat interface.&#x20;

### <mark style="color:purple;">**1. Deploy AIM**</mark>

* Goto local PC web browser and open:

<mark style="color:yellow;"><http://LAN-IP:8006/aims></mark>

* Use search box, type *<mark style="color:yellow;">**lite**</mark>* to display the “litellm-aim”.
* Click on *<mark style="color:blue;">**View**</mark>*
* This will provide AIM Details. &#x20;
  * Under <mark style="color:yellow;">**Select tag**</mark>, choose version <mark style="color:yellow;">l</mark><mark style="color:yellow;">**atest**</mark>
  * Note the "GPUs: 0+" under Tag Details. This tells us the AIM will use a GPU if present and needed but not mandatory for deploying this aim.
  * Under *AIM Environments*, note the <mark style="color:orange;">DEFAULT\_MODEL</mark> and <mark style="color:orange;">OPENAI\_API\_KEY</mark> fields. By default it is <mark style="color:$success;">gpt-3.5-turbo</mark> with no api key.&#x20;
  * For the purpose of this exercise you will generate your own OpenAI API key using this URL:
    * <https://platform.openai.com/settings/organization/api-keys>
      * You will need to open an account (or use existing), add funds ($10 is more than enough) and then "Create new secret key".&#x20;
      * Calls made to this API are very cheap, i.e. 10,000 tokens (\~50 medium complex queries) cost $0.08&#x20;
    * Once you have your API key, store it for your records and copy it into the <mark style="color:orange;">OPEN\_API\_KEY</mark> field. Make sure to take "None" out of the field prior to paste.&#x20;
* The node has a range of ports available for aim deployments. Starting with 9000 and going to 9100. The first aim will take port 9000, the second 9001, and so on. The aim slot number is the last number of the port, i.e. port 9000, slot = 0.
* Click on *<mark style="color:green;">**Deploy**</mark>*
  * Note: if you deploy the default model and later want to change it, simply come back to your running AIM and modify the DEFAULT\_MODEL. The service will restart. You can also choose to wrap any of the other available models given you provide API key.&#x20;
* This will initiate downloading the aim image and starting up the aim. Depending on their size (listed under AIM Details), some aim images take a while to download. You can click on the **Back** button to view the deployed machines and their status.&#x20;
  * If you get a "download failed" message, go back to the main AIMs page and click "Retry" under the deployed machines list. This AIM in particular is 80.2MB.

<mark style="color:orange;">Alternate command line AIM deploy method</mark>

{% code overflow="wrap" %}

```
curl http://localhost:8005/add_aim -d '{"name": "litellm-aim", "tag": "latest", "port": 9000}'
```

{% endcode %}

### <mark style="color:purple;">**2. Setup Ollama web UI**</mark>

<mark style="color:red;">NOTE:</mark> If you've already setup your Ollama web UI for the [Ollama AIM exercise](/hypercycle-cbno/u57KauJomd55OVuTYz6e/hypercycle-aim-deployment/deploy-ollama-aim-w-ui-and-usdc-payments.md), you can skip this section and simply refresh your UI web page to interact with your wrapped litellm model.&#x20;

* Via command line you'll be creating an install script that clones a public GitHub repo and sets up the Ollama web UI via a vite/npm web server running in a tmux session.&#x20;
  * Install script will prompt you for your UI host IP and AIM host IP. You can install this on the same machine that runs your node, or on another machine running the Ubuntu OS on the same network (unless you open up port forwarding/firewall for traversal across Internet). Make sure you are in your home directory, i.e., "/home/hyperai".&#x20;
* Copy and paste the block below directly into the terminal. It will create a file called "<mark style="color:yellow;">ollama-ui-install.sh</mark>":

{% code overflow="wrap" %}

```
curl -L -o ollama-ui-install.sh \
  https://raw.githubusercontent.com/cybershaman73/ollama-aim-ui/refs/heads/main/ollama-ui-install.sh
```

{% endcode %}

* After creating the file, we'll make it executable and run it:

```
chmod +x ollama-ui-install.sh
./ollama-ui-install.sh
```

* After installation, you will see a status message with further direction on how to interact with the web UI server's tmux session, including how to stop and restart it.&#x20;
* If you do not stop the tmux session, the UI server will continue running after exiting the command shell session. tmux sessions do not persist past system restarts.&#x20;

### <mark style="color:purple;">**3. Access the Ollama UI**</mark>

Now it's time to chat!!&#x20;

During the web UI install process, you provided the web port for the UI server. For the purpose of this example, we'll assume you installed the UI on the same machine running the node:

<mark style="color:yellow;"><http://LAN-IP:8880></mark>

* This opens the web page. There's a MetaMask wallet connector in the upper right corner. Upon wallet connect you'll be prompted for a signature (nonce, no fee).&#x20;

<figure><img src="https://4185285616-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FvxiQetCBl3kDURBqm0ta%2Fuploads%2F7bMimg5T0d7e4w3niiIr%2Flite-llm-UI-scrnshot.png?alt=media&amp;token=a260c5ab-23f7-4490-9bfe-0f089a3c0136" alt=""><figcaption></figcaption></figure>

* The page will open listing the active model and chat box. You can ignore the Model drop down in the top left for this exercise, there's only ever one model loaded.&#x20;
* As a node operator, you have control over the cost of these AIM calls. By default, this AIM charges each call at $0.02. For testing, you can also set it to zero, under the URI Settings > Paid URIs of the AIM:
  * <http://LAN-IP:8006/aims/0>
    * Scroll down to the "/request GET POST" URI.
    * Click on "Suggested currencies:" and choose USDC and click the plus sign.&#x20;
    * Make it "Fixed" and assign the cost. <mark style="color:$warning;">This value is in micro-USDC.</mark> For example, to make the cost value 1 USDC, you enter "1000000"&#x20;
    * Click on "Update Cost"&#x20;

<figure><img src="https://4185285616-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FvxiQetCBl3kDURBqm0ta%2Fuploads%2FbQqVzjuS0IUANKiGRqUJ%2Faim-cost-scrnshot.png?alt=media&amp;token=99f89f17-ef3e-4f57-baa6-3125ae6b51a5" alt=""><figcaption></figcaption></figure>

* You can make <mark style="color:$success;">ETH/USDC</mark> deposits to the node manager via the "Add Funds" button on the top menu. Once the Tx settles on chain, you'll see the "USDC:" balance update.&#x20;
* Depending on the complexity of your chat request processing times vary from 10secs to 20secs depending on your Internet connection as the processing is handled by the API hosting the model, not local (unless you choose a local ollama instance as your model). Here's some test queries to run:
  * Knowledge / recall:

    “List the layers of Earth’s atmosphere and typical altitude ranges for each in km.”

    “Summarize the purpose of the ionosphere in 2 bullet points.”
  * Reasoning / math:

    “If a satellite orbits at 400 km altitude with speed 7.7 km/s, estimate its orbital period in minutes.”
  * Robustness:

    “Return a JSON object {‘layers’: \[name, min\_km, max\_km]} for Earth’s atmosphere. No extra text.”
