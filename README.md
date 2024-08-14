# nanoRelation

## server

<details><summary>DB(MongoDB)のインストール</summary>

```zsh  
brew tap mongodb/brew
brew install mongodb-community
```
</details>

<details><summary>Python(3.11.5)のライブラリインストール</summary>

```zsh  
cd server
python -m pip install -r requirements.txt
```
</details>

### DBの起動

```zsh
make db-start
```

### serverの起動

```zsh
make server-start
```

### DBの停止

```zsh
make db-stop
```
