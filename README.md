# AI Email Reply Bot

## Description

The AI Email Reply Bot is a Python script that automates the process of reading, processing, and replying to emails using OpenAI's GPT model. It connects to an email account, reads unread emails, and uses AI to generate friendly and informative responses. This bot is suitable for handling basic email communications for educational and testing purposes.

## How It Works

- The bot connects to an email server using the provided credentials.
- It scans for unread emails and processes each one.
- For each email, the bot uses OpenAI's GPT model to generate a reply based on the email's content.
- The generated reply is sent back to the sender of the email.

## ⚠️ Warning

This bot may share email data with OpenAI to generate responses. **Use for educational/testing purposes only.** Do not use with sensitive or confidential information.

## Installation

You can install the AI Email Reply Bot using GitHub:

1. Clone the repository:

    ```bash
    git clone https://github.com/bzm10/AI-Email-Reply-Bot.git
    ```

2. Navigate to the repository directory:

    ```bash
    cd AI-Email-Reply-Bot
    ```

You can also download the code directly from the repository as a ZIP file and extract it to your preferred location.

## Requirements

- **Python 3**
- **[OpenAI API Key](https://openai.com/blog/openai-api)**
- **App Email Password** (for email account access; for example, if using Gmail, you need to generate an [App Password](https://support.google.com/accounts/answer/185833))
- **Packages**: Install the required packages using pip:

    ```bash
    pip install openai python-dotenv
    ```

## Examples of Use

Below is an example of the bot in action:

- ### Incoming Email:
  **Subject: Math Question for You**

  Hi John Doe,

  I've been working on a math problem and could use your input. If you have a moment, could you help me out with this?

  Given a quadratic equation in the form  ax^2 + bx + c = 0 , how can I determine whether the roots are real or complex? I know the discriminant plays a key role, but I'm a little unsure about how to interpret it.

  I'd appreciate any advice you can offer!

  Thanks,
  Benjamin M
  
- ### Bot's Reply's:
  **Re: Math Question for You**
  
  Hi Benjamin,

  I'd be happy to help you with your math problem.

  To determine whether the roots of a quadratic equation are real or complex, you can use the discriminant (b^2 - 4ac). If the discriminant is positive, then the roots are real and distinct. If the discriminant is zero, then the roots are real and equal. And if the discriminant is negative, then the roots are complex.

  I hope this helps! Let me know if you have any other questions.

  Best,
  John Doe

    

## Example of Logs

The script logs its actions in the terminal, including timestamps, information about unread emails found, the sender's email and subject, and any errors encountered. For example:

```plaintext
[2024-04-30 14:15:23] Found 3 unread emails.
[2024-04-30 14:15:23] From: sender@example.com | Subject: Inquiry
[2024-04-30 14:15:24] Replied to sender@example.com.
[2024-04-30 14:15:25] All unread emails processed.
[2024-04-30 14:20:25] Email from no-reply@accounts.google.com is not allowed.
[2024-04-30 14:20:25] All unread emails processed.
```

