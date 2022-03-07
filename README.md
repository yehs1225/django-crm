# django-crm
A CRM build with django.
Link : https://django-crm.yehs1225.com/
Notes : https://yehs1225.github.io/docs/Django/Build%20a%20CRM%20with%20Django
if you want to run this project locally, you need to :
1.  Create a new file name `.env` in `djcrm` file
2.  Set up `.env` just like `.template.env` file
3.  run `$export READ_DOT_ENV_FILE=True` in the terminal


## 簡介
本專案以django做為後端實作客戶關係系統（CRM）
在首頁進行登入後，該使用者即為組織管理員，
可對Lead及Agent進行操作管理（新增更新刪除），另外使用者也可將Lead指定給Agent。

### Lead
Lead為潛在客戶，由管理者新增並指派給agent。

### Agent
agent依照與lead的關係，可將其分類為Unconverted、converted、contacted等（類別可由組織管理者自行訂定）
新增agent後，預設是會寄送email給agent，使其可以透過重新設定密碼登入系統，但因為**未購買網域信件寄送功能**，因此這部分無法在網頁上操作。
重新設定密碼在本地運行時可在終端機得到
```bash
Content-Type: text/plain; charset="utf-8"
MIME-Version: 1.0
Content-Transfer-Encoding: 7bit
Subject: Password reset on localhost:8000
From: webmaster@localhost
To: agent1@test.com
Date: Mon, 07 Mar 2022 13:39:54 -0000
Message-ID: <164666039446.2955.4846396001119564348@yehs1225-VirtualBox>

You've requested to reset your password.

Please click the following link to enter your new password :

http://localhost:8000/password-reset-confirm/Mg/b1x4mi-03efae05017aca7a6fd529586df4c0f5
```
## Models
Lead、Agent、Category、User、Userprofile
