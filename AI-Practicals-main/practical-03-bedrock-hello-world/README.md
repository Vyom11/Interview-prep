# Complete Practical 3 Guide 
This is a complete start-to-finish guide for your practical, including:

* Creating/configuring AWS credentials
* Installing all required software
* Configuring AWS CLI
* Listing Bedrock models
* Using Converse API with Claude/Titan
* Experimenting with temperature and `top_p`
* Understanding outputs

---

## Practical Objective

You need to:

1. **Install** `boto3`
2. **Configure** AWS CLI
3. **List** available Bedrock foundation models
4. **Invoke** Claude or Titan using Converse API
5. **Experiment** with:
* `temperature` = 0.1 vs 1.0
* Different `top_p` values
* Observe output changes



---

## Part 1 — Create AWS Account

If you already have AWS credentials from your instructor, skip to **Part 5**. Otherwise, create your own AWS account:

1. Open [AWS Sign Up](https://portal.aws.amazon.com/gp/aws/developer/registration/index.html).
2. Create an account with your email, password, and card verification.
3. After verification, login to the [AWS Console](https://console.aws.amazon.com/).

---

## Part 2 — Create IAM User for CLI Access

You should **NOT** use root account credentials. Instead, create an IAM user.

### Step 1 — Open IAM

* Search for **IAM** in the search bar.
* Open the **IAM** dashboard.

### Step 2 — Create User

* Left sidebar: **Users**
* Click: **Create user**
* Example username: `bedrock-user`
* Click: **Next**

### Step 3 — Attach Permissions

1. Choose: **Attach policies directly**
2. Add these permissions:
* `AmazonBedrockFullAccess`
* `IAMReadOnlyAccess`
* *Optional:* `AmazonS3ReadOnlyAccess`


3. Click: **Next** → **Create user**

---

## Part 3 — Generate Access Keys

1. Open the user you just created.
2. Go to: **Security credentials** tab.
3. Scroll to: **Access keys** section.
4. Click: **Create access key**.
5. Select: **Command Line Interface (CLI)**.
6. Tick the confirmation checkbox and click **Next** → **Create access key**.
7. **IMPORTANT:** AWS will show your **Access Key ID** and **Secret Access Key**. Store these safely (CSV download is recommended) as the secret key is shown only once.

---

## Part 4 — Enable Bedrock Model Access

Without this step, Bedrock APIs will fail with access errors.

### Step 1 — Choose Region

* Top-right corner → select: **us-east-1 (N. Virginia)**. This is the primary region for Bedrock features.

### Step 2 — Open Model Access

* Left sidebar: **Model access**
* Click: **Manage model access**

### Step 3 — Enable Models

1. Check the boxes for: **Claude**, **Titan**, **Llama**, and **Cohere**.
2. Click **Submit** or **Request access**.
3. Approval is usually instant but can take a few minutes.

---

## Part 5 — Update Ubuntu

Open your Terminal and run:

```bash
sudo apt update && sudo apt upgrade -y

```

---

## Part 6 — Install Python

1. Check Python version: `python3 --version`
2. Install required tools:
```bash
sudo apt install python3-pip python3-venv -y

```


3. Verify pip: `pip3 --version`

---

## Part 7 — Install AWS CLI

1. Install the CLI:

```bash
    sudo apt install awscli -y
    ```
2.  Verify: `aws --version` (Expected: `aws-cli/2.x.x`)

---

## Part 8 — Create Project Folder
```bash
mkdir aws-bedrock-practical
cd aws-bedrock-practical

```

---

## Part 9 — Create Virtual Environment

1. Create environment:
```bash
python3 -m venv venv

```


2. Activate:

```bash
    source venv/bin/activate
    ```
    *You should now see `(venv)` at the start of your command prompt.*

---

## Part 10 — Install boto3
1.  Install the AWS SDK for Python:
    ```bash
    pip install boto3
    ```
2.  Verify: `pip show boto3`

---

## Part 11 — Configure AWS CLI
Run the configuration command:
```bash
aws configure

```

Enter your details when prompted:

* **AWS Access Key ID:** `[Your Access Key]`
* **AWS Secret Access Key:** `[Your Secret Key]`
* **Default region name:** `us-east-1`
* **Default output format:** `json`

---

## Part 12 — Verify AWS Configuration

Run:

```bash
aws sts get-caller-identity

```

If successful, you will see a JSON output containing your Account ID and User ARN.

---

## Part 13 — Verify Bedrock Access

Run:

```bash
aws bedrock list-foundation-models

```

If you get an `AccessDeniedException`, re-check your IAM permissions and Model Access settings in the AWS Console.

---

## Part 14 — Create Script to List Models

1. Create file: `nano list_models.py`
2. *Paste the script logic provided in your materials.*
3. Save: `CTRL + O`, `ENTER`, `CTRL + X`

---

## Part 15 — Run the Script

```bash
python3 list_models.py

```

---

## Part 16 — Find a Model ID

Look through the output for specific Model IDs. Common examples:

* **Claude:** `anthropic.claude-3-sonnet-20240229-v1:0`
* **Titan:** `amazon.titan-text-express-v1`

---

## Part 17 — Create Converse API Script

1. Create file: `nano converse.py`
2. *Paste the script logic provided in your materials.*
3. Save and exit.

---

## Part 18 — Run Converse Script

```bash
python3 converse.py

```

You should now see an AI-generated response in your terminal!
we find out that when increasing the top p values and temperature the output seems more creative and when the temperature and top p values are at the lower end of the spectrum, the output seems in a fact of the matter manner
```


```
<img width="737" height="559" alt="Screenshot from 2026-05-08 11-38-00" src="https://github.com/user-attachments/assets/7ca544d0-292e-4f4c-b5bb-22d55489649f" />

*the above image is with the temperature and top p both kept at 0.1 resulting in a fact based answer*


<img width="737" height="559" alt="Screenshot from 2026-05-08 11-39-08" src="https://github.com/user-attachments/assets/06a20ac7-7100-4273-98b0-bba04caea79a" />

*the above image is with the updated settings for temperature and top where both are at 1.0*
