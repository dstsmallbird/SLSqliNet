import os

config = {
    "env": {
        "gpu": "7",
        "output_path": "./",
    },
    "model": {
        "train_proportion": 0.6,
        "test_proportion": 0.3,
        "val_proportion": 0.1,
        "epoch_lstm": 100,
        "batch_size_lstm": 256,
        "epoch_bilstm": 150,
        "batch_size_bilstm": 128,
    },
    "datasets": {
        "dimension": 500,
        "albert_dimension": 768,
        "web_app": [
            {
                "type": "time blind",
                "label": 0,
                "file": os.path.abspath("../../dataset/serialization/web_app/time_blind.data"),
                "albert_file": os.path.abspath("../../dataset/word_embedding/web_app/time_blind.data")
            },
            {
                "type": "bool blind",
                "label": 1,
                "file": os.path.abspath("../../dataset/serialization/web_app/bool_blind.data"),
                "albert_file": os.path.abspath("../../dataset/word_embedding/web_app/bool_blind.data")
            },
            {
                "type": "illegal",
                "label": 2,
                "file": os.path.abspath("../../dataset/serialization/web_app/illegal.data"),
                "albert_file": os.path.abspath("../../dataset/word_embedding/web_app/illegal.data")
            },
            {
                "type": "tautology",
                "label": 3,
                "file": os.path.abspath("../../dataset/serialization/web_app/tautology.data"),
                "albert_file": os.path.abspath("../../dataset/word_embedding/web_app/tautology.data")
            },
            {
                "type": "union",
                "label": 4,
                "file": os.path.abspath("../../dataset/serialization/web_app/union.data"),
                "albert_file": [
                    os.path.abspath("../../dataset/word_embedding/web_app/union_0.data"),
                    os.path.abspath("../../dataset/word_embedding/web_app/union_1.data"),
                    os.path.abspath("../../dataset/word_embedding/web_app/union_2.data"),
                    os.path.abspath("../../dataset/word_embedding/web_app/union_3.data")
                ]
            },
            {
                "type": "normal",
                "label": 5,
                "file": os.path.abspath("../../dataset/serialization/web_app/normal.data"),
                "albert_file": [
                    os.path.abspath("../../dataset/word_embedding/web_app/normal_0.data"),
                    os.path.abspath("../../dataset/word_embedding/web_app/normal_1.data"),
                    os.path.abspath("../../dataset/word_embedding/web_app/normal_2.data"),
                    os.path.abspath("../../dataset/word_embedding/web_app/normal_3.data"),
                    os.path.abspath("../../dataset/word_embedding/web_app/normal_4.data"),
                ]

            }
        ],
        "wordpress": [
            {
                "type": "time blind",
                "label": 0,
                "file": os.path.abspath("../../dataset/serialization/wordpress/time_blind_wp.data"),
                "albert_file": os.path.abspath("../../dataset/word_embedding/wordpress/time_blind_wp.data")
            },
            {
                "type": "bool blind",
                "label": 1,
                "file": os.path.abspath("../../dataset/serialization/wordpress/bool_blind_wp.data"),
                "albert_file": os.path.abspath("../../dataset/word_embedding/wordpress/bool_blind_wp.data")
            },
            {
                "type": "illegal",
                "label": 2,
                "file": os.path.abspath("../../dataset/serialization/wordpress/illegal_wp.data"),
                "albert_file": os.path.abspath("../../dataset/word_embedding/wordpress/illegal_wp.data")
            },
            {
                "type": "tautology",
                "label": 3,
                "file": os.path.abspath("../../dataset/serialization/wordpress/tautology_wp.data"),
                "albert_file": os.path.abspath("../../dataset/word_embedding/wordpress/tautology_wp.data")
            },
            {
                "type": "union",
                "label": 4,
                "file": os.path.abspath("../../dataset/serialization/wordpress/union_wp.data"),
                "albert_file": [
                    os.path.abspath("../../dataset/word_embedding/wordpress/union_wp_0.data"),
                    os.path.abspath("../../dataset/word_embedding/wordpress/union_wp_1.data"),
                    os.path.abspath("../../dataset/word_embedding/wordpress/union_wp_2.data"),
                    os.path.abspath("../../dataset/word_embedding/wordpress/union_wp_3.data")
                ]
            },
            {
                "type": "normal",
                "label": 5,
                "file": os.path.abspath("../../dataset/serialization/wordpress/normal_wp.data"),
                "albert_file": [
                    os.path.abspath("../../dataset/word_embedding/wordpress/normal_wp_0.data"),
                    os.path.abspath("../../dataset/word_embedding/wordpress/normal_wp_1.data"),
                    os.path.abspath("../../dataset/word_embedding/wordpress/normal_wp_2.data"),
                    os.path.abspath("../../dataset/word_embedding/wordpress/normal_wp_3.data"),
                    os.path.abspath("../../dataset/word_embedding/wordpress/normal_wp_4.data"),
                    os.path.abspath("../../dataset/word_embedding/wordpress/normal_wp_5.data")
                ]
            }
        ],
    },
    "train_set": {
        "web_app": {
            "data": os.path.abspath("../../dataset/train/train_set.data"),
            "label": os.path.abspath("../../dataset/train/train_set.label"),
            "albert_data": [
                os.path.abspath("../../dataset/train/albert_train_set_0.data"),
                os.path.abspath("../../dataset/train/albert_train_set_1.data"),
                os.path.abspath("../../dataset/train/albert_train_set_2.data"),
                os.path.abspath("../../dataset/train/albert_train_set_3.data"),
                os.path.abspath("../../dataset/train/albert_train_set_4.data"),
                os.path.abspath("../../dataset/train/albert_train_set_5.data")
            ],
            "albert_label": [
                os.path.abspath("../../dataset/train/albert_train_set_0.label"),
                os.path.abspath("../../dataset/train/albert_train_set_1.label"),
                os.path.abspath("../../dataset/train/albert_train_set_2.label"),
                os.path.abspath("../../dataset/train/albert_train_set_3.label"),
                os.path.abspath("../../dataset/train/albert_train_set_4.label"),
                os.path.abspath("../../dataset/train/albert_train_set_5.label"),
            ]
        },
        "wordpress": {
            "data": os.path.abspath("../../dataset/train/train_set_wp.data"),
            "label": os.path.abspath("../../dataset/train/train_set_wp.label"),
            "albert_data": [
                os.path.abspath("../../dataset/train/albert_train_set_wp_0.data"),
                os.path.abspath("../../dataset/train/albert_train_set_wp_1.data"),
                os.path.abspath("../../dataset/train/albert_train_set_wp_2.data"),
                os.path.abspath("../../dataset/train/albert_train_set_wp_3.data"),
                os.path.abspath("../../dataset/train/albert_train_set_wp_4.data"),
                os.path.abspath("../../dataset/train/albert_train_set_wp_5.data"),
                os.path.abspath("../../dataset/train/albert_train_set_wp_6.data"),
            ],
            "albert_label": [
                os.path.abspath("../../dataset/train/albert_train_set_wp_0.label"),
                os.path.abspath("../../dataset/train/albert_train_set_wp_1.label"),
                os.path.abspath("../../dataset/train/albert_train_set_wp_2.label"),
                os.path.abspath("../../dataset/train/albert_train_set_wp_3.label"),
                os.path.abspath("../../dataset/train/albert_train_set_wp_4.label"),
                os.path.abspath("../../dataset/train/albert_train_set_wp_5.label"),
                os.path.abspath("../../dataset/train/albert_train_set_wp_6.label"),
            ]
        }
    },
    "test_set": {
        "web_app": {
            "data": os.path.abspath("../../dataset/test/test_set.data"),
            "label": os.path.abspath("../../dataset/test/test_set.label"),
            "albert_data": [
                os.path.abspath("../../dataset/test/albert_test_set_0.data"),
                os.path.abspath("../../dataset/test/albert_test_set_1.data"),
                os.path.abspath("../../dataset/test/albert_test_set_2.data")
            ],
            "albert_label": [
                os.path.abspath("../../dataset/test/albert_test_set_0.label"),
                os.path.abspath("../../dataset/test/albert_test_set_1.label"),
                os.path.abspath("../../dataset/test/albert_test_set_2.label"),
            ]
        },
        "wordpress": {
            "data": os.path.abspath("../../dataset/test/test_set_wp.data"),
            "label": os.path.abspath("../../dataset/test/test_set_wp.label"),
            "albert_data": [
                os.path.abspath("../../dataset/test/albert_test_set_wp_0.data"),
                os.path.abspath("../../dataset/test/albert_test_set_wp_1.data"),
                os.path.abspath("../../dataset/test/albert_test_set_wp_2.data"),
                os.path.abspath("../../dataset/test/albert_test_set_wp_3.data"),
            ],
            "albert_label": [
                os.path.abspath("../../dataset/test/albert_test_set_wp_0.label"),
                os.path.abspath("../../dataset/test/albert_test_set_wp_1.label"),
                os.path.abspath("../../dataset/test/albert_test_set_wp_2.label"),
                os.path.abspath("../../dataset/test/albert_test_set_wp_3.label"),
            ]
        }
    },
    "val_set": {
        "web_app": {
            "data": os.path.abspath("../../dataset/val/val_set.data"),
            "label": os.path.abspath("../../dataset/val/val_set.label"),
            "albert_data": [
                os.path.abspath("../../dataset/val/albert_val_set.data")
            ],
            "albert_label": [
                os.path.abspath("../../dataset/val/albert_val_set.label")
            ]
        },
        "wordpress": {
            "data": os.path.abspath("../../dataset/val/val_set_wp.data"),
            "label": os.path.abspath("../../dataset/val/val_set_wp.label"),
            "albert_data": [
                os.path.abspath("../../dataset/val/albert_val_set_wp_0.data"),
                os.path.abspath("../../dataset/val/albert_val_set_wp_1.data"),
            ],
            "albert_label": [
                os.path.abspath("../../dataset/val/albert_val_set_wp_0.label"),
                os.path.abspath("../../dataset/val/albert_val_set_wp_1.label"),
            ]
        }
    }
}
