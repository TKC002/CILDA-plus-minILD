# 概要
[敵対的学習を用いた知識蒸留への中間層蒸留と対照学習の導入](https://www.anlp.jp/proceedings/annual_meeting/2023/pdf_dir/Q3-2.pdf)で紹介した手法であるCILDA+minILDのソースコードです。
他にも通常の知識蒸留、RAIL-KD、MATE-KD、CILDAを試せます。
言語モデルはRoBERTa、BERT、BARTに対応しています。BARTはCILDA+minILDに対応していません。

## 対応している手法
Yamlファイルのmethod欄に()内の形式で記入してください。言語モデルによって記入方法が変わる場合は「BERT, RoBERTa : RAIL_c, BART : Bart_RAIL_c」のように言語モデル：記入方法の順で記載しています。
- Without KD (normal)
- Vanilla KD (KD)
- RAIL-KD (BERT, RoBERTa : RAIL_c, BART : Bart_RAIL_c)
- MATE-KD (MATE)
- CILDA (BERT, RoBERTa : CILDA, BART : Bart_CILDA)
- CILDA+minILD (BERT, RoBERTa : CILDA+minILD)

# 環境
python 3.10
Ubuntu
Cuda

## PyTorchのインストール
Pytorchの公式サイトよりCUDAを用いるものをインストールしてください

## その他ライブラリのインストール
pip install -r requirement.txt

# 使用方法
## Generatorを用いない手法
accelerate one_method.py --config YOURCONFIG.yaml
## Generatorを用いる手法(MATE-KD、CILDA、CILDA+minILD)
accelerate mate_training.py --config YOURCONFIG.yaml

# YAMLファイル
CILDA.yaml等を参考にしてください
## 必須
### 知識蒸留でない場合
- model
    - AutoModelForSequenceClassification.from_pretrained()への引数となります。
### 知識蒸留の場合
- teacher
    - AutoModelForSequenceClassification.from_pretrained()への引数となります。
- student
    - AutoModelForSequenceClassification.from_pretrained()への引数となります。
### 知識蒸留であるかに関わらず
- mathod
    - 使用する手法を指定します。
    - 知識蒸留でないならばnormal
    - KD, RAIL_c, MATE, CILDA, CILDA_minILDに対応しています。
- tokenizer
    - AutoTokenizer.from_pretrained()への引数となります。
- tasks
    - GLUEのタスクのみ対応
- data_ratio
    - 0以上1以下の数
    - タスクのデータのうちどれだけの割合を使用するかを決定します。
- lr_scheduler_type
    - constantのみ対応しています
- wd
    - weight_decay
- num_warmup_steps 
- batch_size
    - 1つのgpuあたりのバッチサイズです
- device_num
    - 使用するgpuの数です
- epochs
    - 何エポック学習するかを決定します
- num_of_ex
    - 同じ設定で何回実験を繰り返すかを決定します
- pad_to_max_length
    - max_lengthと記入してください。
- max_length
    - 1データのトークンの最大の長さです。
- lr
    - 学習率
    - 配列で指定してください。
- outdir
    - 結果を保存するディレクトリを指定します。
- model_name
    - RoBERTaならroberta, BERTならbert, BARTならbartと記入してください。
### 手法によっては必須
- lambdas
    - 損失関数の割合
    - KDでは[0.5, 0.5]がデフォルト値ですが、その他の手法では指定する必要があります。
- n_generator_iter
    - Generatorを用いる手法で使います。最大化ステップのステップ数を指定します。指定しないと10となります。
- alpha
    - CILDAの最大化ステップにおける損失関数にかけるハイパーパラメータです
- alpha2
    - Trueの場合、$L_{CRD}$の係数に$\frac{1}{\log K}$をかけます。$K$はバッチサイズです。
- linear
    - 中間層を使う手法において、中間層の出力を線形変換した後の次元数です
- linear_method
    - trainingと記入してください

- lambda_nume
    - CILDA_minILDの最小化ステップでの損失関数にかけるハイパーパラメータの分子です
- lambda_deno
    - CILDA_minILDの最小化ステップでの損失関数かけるハイパーパラメータの分母です
    - lambda[i] = lambda_nume[i]/lambda_deno[i]となります。


### 任意
- neptune関連
    - use_neptune
        - neptune.aiでログを取るかをTrue, Falseで指定します。指定がない場合、Trueとなります。
    - nep_proj
        - neptune.aiを使用する際のプロジェクトの名前です
    - nep_method
        - neptune.aiへ結果を保存するときのmethodと言うパラメータに保存する値です
    - nep_token
        - neptume.aiのプロジェクトにアクセスするためのトークンです。
