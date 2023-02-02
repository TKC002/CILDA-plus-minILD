# 概要
CILDA+minILDのソースコード
## 対応している手法
- Without KD (normal)
- Vanilla KD (KD)
- RAIL-KD (BERT, RoBERTa : RAIL_c, BART : Bart_RAIL_c)
- MATE-KD (MATE)
- CILDA (BERT, RoBERTa : CILDA, BART : Bart_CILDA)
- CILDA+minILD (BERT, RoBERTa : CILDA+minILD)

# 環境
python 3.10

## PyTorchのインストール
公式サイトよりCUDAを用いるものをインストール

## その他ライブラリのインストール
pip install -r requirement.txt

# 使用方法
## Generatorを用いない手法
accelerate one_method.py --config YOURCONFIG.yaml
## Generatorを用いる手法
accelerate mate_training.py --config YOURCONFIG.yaml

# YAMLファイル
## 必須
### 知識蒸留でない場合
- model
    - AutoModelForSequenceClassification.from_pretrained()への引数となる。
### 知識蒸留の場合
- teacher
    - AutoModelForSequenceClassification.from_pretrained()への引数となる。
- student
    - AutoModelForSequenceClassification.from_pretrained()への引数となる。
### 知識蒸留であるかに関わらず
- mathod
    - 使用する手法を指定する。
    - 知識蒸留でないならばnormal
    - KD, RAIL_c, MATE, CILDA, CILDA_minILDに対応している。
- tokenizer
    - AutoTokenizer.from_pretrained()への引数となる。
- tasks
    - GLUEのタスクのみ対応
- data_ratio
    - 0以上1以下の数
    - タスクのデータのうちどれだけの割合を使用するかを決定する。
- lr_scheduler_type
    - constantのみ対応
- wd
    - weight_decay
- num_warmup_steps 
- batch_size
    - 1つのgpuあたりのバッチサイズ
- device_num
    - 使用するgpuの数
- epochs
    - 何エポック学習するか
- num_of_ex
    - 同じ設定で何回実験を繰り返すか
- pad_to_max_length
    - tokenizerのpaddingの設定
- max_length
    - tokenizerのpaddingの設定
- lr
    - 学習率
    - 配列で指定
- outdir
    - 結果を保存するディレクトリを指定する。
- model_name
    - RoBERTaならroberta, BERTならbert, BARTならbartと記入
### 手法によっては必須
- lambdas
    - 損失関数の割合
    - KDでは[0.5, 0.5]がデフォルト値であるが、その他の手法では指定する必要がある。
- n_generator_iter
    - Generatorを用いる手法で使う。最大化ステップのステップ数を指定する。指定しないと10となる。
- alpha
    - CILDAの最大化ステップにおける損失関数の割合
- alpha2
    - Trueの場合、$L_{CRD}$の係数に$\frac{1}{\log K}$をかける。$K$はバッチサイズである。
- linear
    - 中間層を使う手法において、中間層の出力を線形変換した後の次元数
- linear_method
    - trainingと記入

- lambda_nume
    - CILDA_minILDの最小化ステップでの損失関数の割合の分子
- lambda_deno
    - CILDA_minILDの最小化ステップでの損失関数の割合の分母
    - lambda[i] = lambda_nume[i]/lambda_deno[i]となる。


### 任意
- use_neptune
    - neptune.aiでログを取るかをTrue, Falseで指定。指定がない場合、Trueとなる。
- nep_proj
    - neptune.aiを使用する際のプロジェクトの名前
- nep_method
    - neptune.aiへ結果を保存するときのmethodと言うパラメータに保存する値
- nep_token
    - neptume.aiのプロジェクトにアクセスするためのトークン
