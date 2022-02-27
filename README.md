# ps5-crawler

## Usage

1. LINE Notify でアカウント登録.  
   https://notify-bot.line.me/ja/

2. アクセストークンの発行し, `src/line/access_token.txt` にペースト.

3. Google Cloud Functions にデプロイ.
   ```shell
   sh deploy.sh
   ```

参考: https://notify-bot.line.me/doc/ja/
