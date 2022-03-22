## netdevpyについて

### 概要
- netdevpyは、パラメータシートからコンフィグ、またはコンフィグからパラメータシート間の変換を行うPythonツールです。

### 仕組み
- パラメータシートからコンフィグを作成するためには、以下の三点が必要です。
    1. パラメータを記述した**パラメータシート**
    2. パラメータシートのどこからパラメータを取得するのかを記述した**ルールファイル**
    3. パラメータシートに記述されない共通のコンフィグを記載した**コンフィグサンプルファイル**
- パラメータシートからルールファイルに基づいてパラメータを取得し、コマンドへと変換後、コンフィグサンプルファイルを用いてコンフィグを作成します。


## netdevpyのインストール方法
### Pythonインタープリタで実行する場合
1. ```git clone```により、本リポジトリをコピーする。
```
C:\>git clone https://github.com/TomoyaKamei/netdevpy.git
```
2. ```python -m venv (仮想環境名)```により、pythonの仮想環境を作成する。
```
C:\>cd netdevpy
C:\netdevpy>python -m venv venv
```
3. 仮想環境を起動する。
```
C:\netdevpy>./venv/Script/activate
(venv)C:\netdevpy>
```

4. ```pip install -r requirements.txt```により、pythonの仮想環境に必要なパッケージをインストールする。
```
(venv)C:\netdevpy>pip install -r requirements.txt
```

### .exeファイル形式で実行する場合
- ※前節のPythonインタープリタで実行する方法を事前に実行して下さい。
1. pyinstallerを使用して.exeファイル化する。作成されたファイルは、/dist配下に存在する。
```
(venv)C:\netdevpy>make build
```
2. 必要な場合、環境変数を通す。
```
(venv)C:\netdevpy>SET PATH=%PATH%;C:\netdevpy\dist
```

## netdevpyの使用方法

### パラメータシートからコンフィグの作成
- 以下の書式で実行する。
    - ```-cs, --config_sample```は、コンフィグサンプルが存在するパスを指定する。
    - ```-ps, --parameter_sheet```は、パラメーターシートが存在するパスを指定する。
    - ```-rf, --rule_file```は、ルールファイルが存在するパスを指定する。
    - ```-op, --output```は、出力するコンフィグを格納するパスを指定する。
    - ```-es, --exception_sheet```は、コンフィグ作成に用いないシートを記述する。
- Pythonでの実行例
    ```
    (venv)C:\netdevpy>python netdevpy.py create_config -cs ./data/input/config_sample/wa_config.log -ps ./data/input/parameter_sheets/WA1512パラメータシート.xlsx -rf ./data/input/rule/wa_rule.yml -op ./data/output/config/ -es 改版履歴
    ```
- exeファイルでの実行例
    ```
    (venv)C:\netdevpy\dist>netdevpy create_config -cs ./data/input/config_sample/wa_config.log -ps ./data/input/parameter_sheets/WA1512パラメータシート.xlsx -rf ./data/input/rule/wa_rule.yml -op ./data/output/config/ -es 改版履歴
    ```

### コンフィグからパラメーターシートの更新
- ※未実装


## netdevpyの簡易リファレンス

### Ruleファイル
#### 概要
- Ruleファイルは、主にパラメータシートのどこからパラメータを取得するのかを記述したファイルになります。
#### パラメータ解説
- Ruleファイルのパラメータは以下の通りである。
    - ```common_parameter```
        - ```filling```
            - (Optional)パディングで使用する記号を指定します。デフォルトは```!```です。
    - ```converter_rules```
        - ```ルール名```
            - (Required)ルール名を記載します。
            - 任意の文字列で問題ありませんが、ルール名が混在しないようにして下さい。
                - ```description``` 
                    - (Optional)ルールの概要について記載する場所です。
                - ```marker```
                    - (Required)コンフィグサンプルでの挿入位置を決定するマーカーを記述します。
                    - マーカーは```%%(marker名)%%```という書式で記載される必要があります。
                - ```data```
                    - (Required)パラメーターシート上におけるパラメータの位置を記載する場所です。
                        - ```parameter_column_locations```
                            - (Required)パラメータのカラム(列)方向の位置を記載する場所です。
                                - ```name```
                                    - (Required)パラメータ名について記載する場所です。
                                - ```column_number```
                                    - (Required)パラメータが存在する列を記載する場所です。
                                    - カラム番号は、アルファベットの組み合わせである必要があります。
                        - ```row_from```
                            - (Required)パラメータの行の始端を記載する場所です。
                            - row_fromは、数字である必要があります。
                        - ```row_to```
                            - (Required)パラメータの行の終端を記載する場所です。
                            - row_toは、数字である必要があります。
                - ```commands```
                    - (Required)本ルールで生成するコマンド群について記載する場所です。
                    - 基本的には```command xxxx {パラメータ名}```のように、```{パラメータ名}```を用いる事で動的に値を変更します。
                    - パラメータ名は、parameter_column_locationsのnameと同じものを使用して下さい。
                - ```validations```
                    - (Optional)取得した値が一定の形式に準じて作成されているかを判定するために使用します。
                    - ※未実装
                - ```conditions```
                    - (Optional)取得した値によってコマンドの内容を変更したい場合に使用します。
                        - ```condition```
                            - (Required)取得した値によってコマンドの内容を変更する場合の条件を記述する場所です。
                                - ```type```
                                    - (Required)条件を記述箇所です。
                                    - 現在使用できる値は、```isContained```または、```isEmpty```のみです。
                                - ```target_parameter```
                                    - (Required)判定に用いるパラメータ名のリストを記述する箇所です。
                                - ```target_string```
                                    - (Optional)判定に用いる文字列を記述する箇所です。
                                    - ```isContained```の場合に用いる。
                        - ```action```
                            - (Required)条件がTrueの場合に行う処理を記述する場所です。
                            - 現在使用できる値は、```Add```または、```Delete```のみです。
                        - ```commands```
                            - (Required)条件満たされた場合に対象となるコマンドのリストを記述する場所です。
                            - converter_rulesのcommandsと同様に記述して下さい。
                - ```options```
                    - (Optional)
                        - ```indent_level```
                            - (Optional)コマンドに適用される基本的なインデントレベルです。
                            - デフォルトは0です。
                        - ```filling_each_commands```
                            - (Optional)パディングを1つのコマンドごとに打つかどうかを決定する場所です。
                            - デフォルトはFalseです。
                        - ```filling_each_commands_group```
                            - (Optional)パディングを1つのコマンドグループごとに打つかどうかを決定する場所です。
                            - デフォルトはFalseです。
#### 記述例
```yml
common_parameter:
  filling: "!"
converter_rules:
  HOSTNAME:
    description: "ホスト名"
    marker: "%%host_name%%"
    data:
      parameter_column_locations: 
        - name: "HostName"
          column_number: "D"
      row_from: 9
      row_to:   9
    commands: 
      - "hostname {HostName}"
    validations: []
    conditions: []
    options:
      indent_level: 0
      filling_each_commands: False
      filling_each_commands_group: False
  DETOUR_VLAN:
      description: "VLAN番号"
        ...(省略)...
```
### ConfigSampleファイル
#### 概要
- ConfigSampleファイルは、どこにコマンドを挿入するか、またはパラメータシートに記述されていないコンフィグを記載するファイルです。
- コマンドを挿入する箇所に```%%マーカー名%%```を記載して下さい。
#### 記述例
```log
syslog destination 172.x.x.x
syslog enable
syslog function all warning
!
%%host_name%%
!
!
!
!
no wireless-adapter enable
!
bridge ieee enable
!
device usb0
!
device module0
!
!
interface GigaEthernet0.0
  %%detour_vlan%%
  %%ltert_vlan%%
  no ip address
  no shutdown
!
        ...(省略)...
```
### ParameterSheetファイル
#### 概要
- ParameterSheetファイルは、パラメータを格納するファイルです。

## その他
### 今後の追加機能
- v1.1.1
    - validationの追加
- v1.1.2
    - ログの追加
- v1.2.0
    - コンフィグ→パラメータシート間の変換実装
- v2.0.0
    - GUI化
### バグなど発見した場合
