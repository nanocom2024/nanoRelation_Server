# DB schema

## users

- ユーザー情報の管理

```json
{
  "uid": "user_uid",
  "name": "username",
  "email": "test@test.org",
  "name_id": "#1111",
  "token": "eyJhbGciOiJIUzI1NiI..."
}
```

- uid
  - ユーザー固有のuid
  - Firebase Authentication によって生成される
- name
  - ユーザー名
- email
  - メールアドレス
- name_id
  - 同じユーザー名のユーザーを識別するための識別子
- token
  - 認証で用いる文字列
  - ログインした時などに再生成される

## device_keys

- サーバーで生成したデバイス用の秘密鍵, 公開鍵, major, minorの管理

```json
{
  "uid": "device_uid",
  "private_key": "private_key",
  "public_key": "public_key",
  "major": "major",
  "minor": "minor"
}
```

- uid
  - デバイスから送信された固有のuid
- private_key
  - 秘密鍵（Ed25519）
- public_key
  - 公開鍵（Ed25519）
- major
  - unsigned Int (16bit)
  - iBeaconに準拠
- minor
  - unsigned Int (16bit)
  - iBeaconに準拠

## pairings

- ユーザーとデバイス間のペアリングの管理

```json
{
  "uid": "user_uid",
  "private_key": "private_key",
  "public_key": "public_key",
  "major": "major",
  "minor": "minor"
}
```

- uid
  - users (uid)
- private_key
  - device_keys (private_key)
- public_key
  - device_keys (public_key)
- major
  - device_keys (major)
- minor
  - device_keys (minor)

## children

- ユーザーの子供を管理

```json
{
  "parent_uid": "user_id",
  "children": [
    "child1_uid",
    "child2_uid",
  ]
}
```

- parent_uid
  - users (uid)
- children
  - 子供のユーザーidのリスト
  - list(users (uid))

## notification_config

- 通知設定の管理

```json
{
  "owner": "user_id",
  "disables": [
    "disable_user_id"
  ]
}
```

- owner
  - users (uid)
- disables
  - list(users (uid))
  - disablesに追加されたユーザーとの通知は無効になる

## pre_passes

- 仮すれ違い状態ユーザーの管理
- 30秒間一方向のすれ違い情報を保持

```json
{
  "sent_uid": "user_uid1",
  "received_uid": "user_uid2",
  "created_at": "yyyy-mm-ddThh:mm:ss.000Z"
}
```

- sent_uid
  - users (uid)
  - ビーコン受信ユーザー
- received_uid
  - users (uid)
  - ビーコン送信ユーザー
- created_at
  - 最初の一方向すれ違い時間

## now_passes

- 現在すれ違い状態ユーザーの管理
- 60秒間すれ違い情報を保持

```json
{
  "uid1": "user_uid1",
  "uid2": "user_uid2",
  "timestamp": 1727076790.302931
}
```

- uid1
  - users (uid)
  - min(uid)
- uid2
  - users (uid)
  - max(uid)
- timestamp
  - 初回の双方向すれ違い時間

## lost_children

- 迷子状態の子供を管理

```json
{
  "major": "46374",
  "minor": "46577"
}
```

- major
  - device_keys (major)
- minor
  - device_keys (minor)

## log_passes

- すれ違いの履歴を保存

```json
{
  "uid1": "user_uid1",
  "uid2": "user_uid2",
  "timestamp": 1727076790.302931
}
```

- uid1
  - now_passes (uid1)
- uid2
  - now_passes (uid2)
- timestamp
  - now_passes (timestamp)
  - 相互すれ違い状態になった時間

## log_own

- 自身のデバイスが近くにあった履歴

```json
{
  "owner_uid": "user_uid",
  "timestamps": [
    1727091356.524546,
    1727338519.360263,
    ...
  ]
}
```

- owner_uid
  - users (uid)
- timestamps
  - list(timestamp)
  - 自身のデバイスが近くにある時の時間
  - 最低間隔は1分

## log_near_own_children

- 子供のデバイスが近くにあった履歴

```json
{
  "parent_uid": "parent_uid",
  "child_uid": "child_uid",
  "timestamps": [
    1727092418.162974,
    1727092449.213103,
    ...
  ]
}
```

- parent_uid
  - users (uid)
  - 親ユーザーのuid
- child_uid
  - users (uid)
  - 子ユーザーのuid
- timestamps
  - list(timestamp)
  - 子供のデバイスを検知した時間
  - 最低間隔は30秒

## log_lost_passes

- 迷子とすれ違った履歴

```json
{
  "owner_uid": "user_uid",
  "child_uid": "child_uid",
  "timestamps": [
    {
      "timestamp": 1727932476.521881,
      "latitude": ddd.18461483747083,
      "longitude": ddd.1109323932675
    }
  ]
}
```

- owner_uid
  - users (uid)
  - 迷子とすれ違ったユーザー
- child_uid
  - users (uid)
  - 迷子だったユーザー
- timestamps
  - list(json)
  - timestamp
    - 迷子とすれ違った時間
  - latitude
    - float
    - すれ違った緯度
  - longitude
    - float
    - すれ違った経度

## log_lost_children

- 迷子アラートの履歴

```json
{
  "child_uid": "user_uid",
  "messages": [
    {
      "msgID": "694D771D-DEEC-4199-B673-DA126E840D0E",
      "text": "迷子アラートを発信しました",
      "tag": "start",
      "timestamp": 1726976111.7599401
    },
    ...
  ]
}
```

- child_uid
  - users (uid)
- messages
  - list(json)
  - msgID
    - メッセージを識別するid
  - text
    - アプリに表示されるテキスト
  - tag
    - アプリ内でメッセージの種類を識別するためのタグ
  - timestamp
    - メッセージが作成された時間
