# SLSqliNet

## Directory Structure
```
|-- SLSqliNet
    |-- dataset
    |   |-- test
    |   |-- train
    |   |-- val
    |   |-- word_embedding
    |-- detection
    |   |-- bilstm
    |   |-- bilstm_attention
    |   |-- double_bilstm
    |   |-- double_bilstm_attention
    |   |-- double_lstm
    |   |-- lstm
    |   |-- svm
    |   |-- utils
    |-- src
        |-- config
        |-- generalize
        |   |-- colx
        |-- middleware
        |-- utils
        |-- word_embedding
```
- dataset
   - **word_embedding**: pretrained sentence vectors by using Albert model
   - **train/test/val**: train/test/validation set of pretrained dataset, proportion: 6:3:1
- detection dir
   - **utiles**: split raw dataset to train/test/validation set, load dataset in model training period and evaluate the model performance
   - **other folders**: different model training and evaluation result
- src dir
   - **middleware**: middleware for listening and forwarding communication traffic between Web application and DB
   - **generalize**: parse and generalize SQL statements based on generalizing rule and parser
      - **colx**: MySQL parser based on Golang
   - **word_embedding**: pretrain by using Alber model and generate sentence vectors

## Web Application

1. Run Web Server

```
# src/

python3 server.py
```
Request web application and perform **SQL injection**: call `request()` of src/request_api.py
Perform **normal request** to Web API: call `request_normal_api()` of src/request_api.py


2. Run Middleware

Run middleware to listen and forward communication traffic between Web app and DB:
```
# src/middleware

python3 middleware.py
```

## Dataset Preprocessing

### Generalization
`src/generalize/colx/main.go` implements two structures named *Visitor* to **extract column/table name** of MySQL statements. `colx` and `colx.exe` are executive file for Linux and Windows respectively.

Parse and generalize MySQL statements:

```
# src/generalize/

python3 generalize.py
```

### Pretrain with Albert

```
# src/word_embedding/

python3 init.py
```
`init.py` calls **Pretrain** class of `albert_embedding.py` to generate **sentence vector**.

## Model Training and Evaluation

`detection/utils/evaluate.py`: evaluate model performance.
`detection/utils/data.py`: split raw dataset into train/test/validation set with 6:3:1 proportion.
`detection/utils/config.py`: configure dataset path and other parameters.

Every folders in `detection/` except `utils` contains model file and source code. You can run `.py` file to train and evaluate model, and output accuracy/loss figure, JSON file of evaluation result, JSON file of training history, and model folder.