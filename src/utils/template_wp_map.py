TEMPLATE_WP_MAP = {
    "single_quote": [
        [
            "SELECT option_name, option_value FROM wp_options WHERE autoload = 'yes",
            "'"
        ],
        [
            "SELECT * FROM wp_users WHERE user_login = 'wp",
            "' LIMIT 1"
        ],
        [
            "SELECT option_value FROM wp_options WHERE option_name = 'WPLANG",
            "' LIMIT 1"
        ],
        [
            "SELECT umeta_id FROM wp_usermeta WHERE meta_key = 'rich_editing",
            "' AND user_id = 1"
        ],
        [
            "SELECT ID FROM wp_users WHERE user_nicename = 'wp' AND user_login != 'wp",
            "' LIMIT 1"
        ],
        [
            "SELECT option_value FROM wp_options WHERE option_name = 'can_compress_scripts",
            "' LIMIT 1"
        ],
        [
            "UPDATE `wp_usermeta` SET `meta_value` = 'false' WHERE `user_id` = 1 AND `meta_key` = 'rich_editing",
            "'"
        ],
        [
            "SELECT post_status, COUNT( * ) AS num_posts FROM wp_posts WHERE post_type = 'post",
            "' GROUP BY post_status"
        ],
        [
            "SELECT wp_posts.ID FROM wp_posts WHERE 1=1 AND wp_posts.post_type = 'post",
            "' AND ((wp_posts.post_status = 'publish')) ORDER BY wp_posts.post_date DESC LIMIT 0, 5"
        ],
        [
            "SELECT p.ID FROM wp_posts AS p WHERE p.post_date > '2021-12-10 03:18:59' AND p.post_type = 'post",
            "' AND ( p.post_status = 'publish' OR p.post_status = 'private' ) ORDER BY p.post_date ASC LIMIT 1"
        ],
    ],
    "sindle_quote_1_parenthesis": [
        [
            "SELECT t.*, tt.* FROM wp_terms AS t INNER JOIN wp_term_taxonomy AS tt ON t.term_id = tt.term_id WHERE tt.taxonomy IN ('category",
            "') ORDER BY t.name ASC"
        ],
        [
            "SELECT comment_post_ID, COUNT(comment_ID) as num_comments FROM wp_comments WHERE comment_post_ID IN ( '1",
            "' ) AND comment_approved = '0' GROUP BY comment_post_ID"
        ],
        [
            "SELECT t.*, tt.* FROM wp_terms AS t INNER JOIN wp_term_taxonomy AS tt ON t.term_id = tt.term_id WHERE tt.taxonomy IN ('post_format",
            "') AND tt.count > 0 ORDER BY t.name ASC"
        ],
        [
            "SELECT wp_comments.comment_ID FROM wp_comments JOIN wp_posts ON wp_posts.ID = wp_comments.comment_post_ID WHERE ( comment_approved = '1' ) AND wp_posts.post_status IN ('publish",
            "') ORDER BY wp_comments.comment_date_gmt DESC LIMIT 0,5"
        ],
        [
            "SELECT t.*, tt.*, tr.object_id FROM wp_terms AS t INNER JOIN wp_term_taxonomy AS tt ON t.term_id = tt.term_id INNER JOIN wp_term_relationships AS tr ON tr.term_taxonomy_id = tt.term_taxonomy_id WHERE tt.taxonomy IN ('category', 'post_tag', 'post_format",
            "') AND tr.object_id IN (1) ORDER BY t.name ASC"
        ],
        [
            "SELECT SQL_CALC_FOUND_ROWS wp_posts.ID FROM wp_posts WHERE 1=1 AND wp_posts.post_type = 'post' AND (wp_posts.post_status = 'publish' OR wp_posts.post_status = 'future' OR wp_posts.post_status = 'draft' OR wp_posts.post_status = 'pending' OR wp_posts.post_status = 'private",
            "') ORDER BY wp_posts.post_date DESC LIMIT 0, 20"
        ],
        [
            "SELECT COUNT( 1 ) FROM wp_posts WHERE post_type = 'post' AND post_status NOT IN ( 'trash','auto-draft','inherit','request-pending','request-confirmed','request-failed','request-completed",
            "' ) AND post_author = 2"
        ],
        [
            "SELECT COUNT(*) FROM wp_terms AS t INNER JOIN wp_term_taxonomy AS tt ON t.term_id = tt.term_id WHERE tt.taxonomy IN ('category",
            "')"
        ],
        [
            "SELECT t.*, tt.* FROM wp_terms AS t INNER JOIN wp_term_taxonomy AS tt ON t.term_id = tt.term_id WHERE tt.taxonomy IN ('wp_theme') AND t.name IN ('twentytwentyone",
            "')"
        ]
    ],
    "single_quote_2_parenthesis": [
        [
            "SELECT wp_posts.ID FROM wp_posts WHERE 1=1 AND wp_posts.post_type = 'post' AND ((wp_posts.post_status = 'publish",
            "')) ORDER BY wp_posts.post_date DESC LIMIT 0, 5"
        ],
        [
            "SELECT SQL_CALC_FOUND_ROWS wp_posts.ID FROM wp_posts WHERE 1=1 AND wp_posts.post_type = 'wp_block' AND ((wp_posts.post_status = 'publish",
            "')) ORDER BY wp_posts.post_date DESC LIMIT 0, 100"
        ],
        [
            "SELECT wp_posts.ID FROM wp_posts WHERE 1=1 AND wp_posts.post_parent = 1 AND wp_posts.post_type = 'revision' AND ((wp_posts.post_status = 'inherit",
            "')) ORDER BY wp_posts.post_date DESC, wp_posts.ID DESC"
        ],
        [
            "SELECT wp_posts.* FROM wp_posts WHERE 1=1 AND wp_posts.post_name = '1-autosave-v1' AND wp_posts.ID NOT IN (0) AND wp_posts.post_type IN ('post', 'page', 'attachment') AND ((wp_posts.post_status = 'trash",
            "')) ORDER BY wp_posts.post_date DESC "
        ],
        [
            "SELECT wp_comments.comment_ID FROM wp_comments WHERE ( ( comment_approved = '1' ) OR ( user_id = 1 AND comment_approved = '0",
            "' ) ) AND comment_post_ID = 1 AND comment_parent IN ( 1,2 ) ORDER BY wp_comments.comment_date_gmt ASC, wp_comments.comment_ID ASC"
        ],
        [
            "SELECT SQL_CALC_FOUND_ROWS wp_comments.comment_ID FROM wp_comments WHERE ( ( comment_approved = '1' ) OR ( user_id = 1 AND comment_approved = '0",
            "' ) ) AND comment_post_ID = 1 AND comment_parent = 0 ORDER BY wp_comments.comment_date_gmt ASC, wp_comments.comment_ID ASC"
        ],
        [
            "SELECT wp_users.ID,wp_users.user_login,wp_users.display_name FROM wp_users INNER JOIN wp_usermeta ON ( wp_users.ID = wp_usermeta.user_id ) WHERE 1=1 AND (( wp_usermeta.meta_key = 'wp_user_level' AND wp_usermeta.meta_value != '0",
            "' )) ORDER BY display_name ASC"
        ],
        [
            "SELECT COUNT(*) FROM wp_terms AS t INNER JOIN wp_term_taxonomy AS tt ON t.term_id = tt.term_id WHERE tt.taxonomy IN ('post_tag') AND ((t.name LIKE '%uncategaries%') OR (t.slug LIKE '%uncategaries%",
            "'))"
        ]
    ],
    "single_quote_3_parenthesis": [
        [
            "SELECT post_author, COUNT(*) FROM wp_posts WHERE ( ( post_type = 'post' AND ( post_status = 'publish' OR post_status = 'private",
            "' ) ) ) AND post_author IN (1) GROUP BY post_author"
        ],
        [
            "SELECT post_author, COUNT(*) FROM wp_posts WHERE ( ( post_type = 'post' AND ( post_status = 'publish' OR post_status = 'private",
            "' ) ) ) AND post_author IN (1,2,3,4) GROUP BY post_author"
        ],
        [
            "SELECT wp_posts.ID FROM wp_posts WHERE 1=1 AND wp_posts.post_type = 'post' AND ((wp_posts.post_author = 3 AND (wp_posts.post_status = 'future",
            "'))) ORDER BY wp_posts.post_date ASC LIMIT 0, 5"
        ]
    ],
    "num_tail": [
        [
            "UPDATE `wp_posts` SET `comment_count` = 2 WHERE `ID` = 1", ""
        ],
        [
            "SELECT comment_ID FROM wp_comments WHERE comment_post_ID = 7", ""
        ],
        [
            "UPDATE `wp_posts` SET `guid` = 'http://172.16.44.88/?p=5' WHERE `ID` = 5", ""
        ],
        [
            "SELECT meta_id FROM wp_postmeta WHERE meta_key = '_edit_lock' AND post_id = 1", ""
        ],
        [
            "SELECT COUNT(*) FROM wp_comments WHERE user_id = 2 AND comment_approved = 1", ""
        ],
        [
            "SELECT umeta_id FROM wp_usermeta WHERE meta_key = 'rich_editing' AND user_id = 1", ""
        ],
        [
            "SELECT term_taxonomy_id FROM wp_term_relationships WHERE object_id = 35 AND term_taxonomy_id = 2", ""
        ],
        [
            "SELECT t.*, tt.* FROM wp_terms AS t INNER JOIN wp_term_taxonomy AS tt ON t.term_id = tt.term_id WHERE t.term_id = 5", ""
        ],
        [
            "SELECT COUNT(*) FROM wp_term_relationships, wp_posts WHERE wp_posts.ID = wp_term_relationships.object_id AND post_status IN ('publish') AND post_type IN ('post') AND term_taxonomy_id = 1", ""
        ],
        [
            "SELECT COUNT(*) FROM wp_comments WHERE comment_author_email = 'wapuu@wordpress.example' AND comment_author = 'A WordPress Commenter' AND comment_author_url = 'https://wordpress.org/' AND comment_approved = 1", ""
        ],
        [
            "SELECT COUNT( 1 ) FROM wp_posts WHERE post_type = 'post' AND post_status NOT IN ( 'trash','auto-draft','inherit','request-pending','request-confirmed','request-failed','request-completed' ) AND post_author = 4", ""
        ],
        [
            "UPDATE `wp_users` SET `user_pass` = '$P$BvutwzeQb1l1cDew1ig36HnATsIIbX0', `user_nicename` = 'wp', `user_email` = '107931@gmail.com', `user_url` = 'http://172.16.44.88', `user_registered` = '2021-12-10 03:18:59', `user_activation_key` = '', `display_name` = 'wp' WHERE `ID` = 1", ""
        ]
    ],
    "num": [
        [
            "SELECT * FROM wp_posts WHERE ID = 3",
            " LIMIT 1"
        ],
        [
            "UPDATE `wp_usermeta` SET `meta_value` = 'false' WHERE `user_id` = 1",
            " AND `meta_key` = 'rich_editing'"
        ],
        [
            "SELECT post_name FROM wp_posts WHERE post_name = 'hello-world' AND post_type = 'post' AND ID != 1",
            " LIMIT 1"
        ],
        [
            "SELECT wp_comments.comment_ID FROM wp_comments WHERE ( ( comment_approved = '1' ) OR ( user_id = 1 AND comment_approved = '0' ) ) AND comment_post_ID = 1",
            " AND comment_parent IN ( 1,2 ) ORDER BY wp_comments.comment_date_gmt ASC, wp_comments.comment_ID ASC"
        ],
        [
            "SELECT SQL_CALC_FOUND_ROWS wp_comments.comment_ID FROM wp_comments WHERE ( ( comment_approved = '1' ) OR ( user_id = 1 AND comment_approved = '0' ) ) AND comment_post_ID = 1",
            " AND comment_parent = 0 ORDER BY wp_comments.comment_date_gmt ASC, wp_comments.comment_ID ASC"
        ]
    ],
    "num_1_parenthesis": [
        [
            "SELECT wp_posts.* FROM wp_posts WHERE ID IN (1",
            ")"
        ],
        [
            "SELECT wp_posts.* FROM wp_posts WHERE ID IN (45,38,1",
            ")"
        ],
        [
            "SELECT term_id, meta_key, meta_value FROM wp_termmeta WHERE term_id IN (2,5",
            ") ORDER BY meta_id ASC"
        ],
        [
            "SELECT post_id, meta_key, meta_value FROM wp_postmeta WHERE post_id IN (3",
            ") ORDER BY meta_id ASC"
        ],
        [
            "SELECT wp_comments.* FROM wp_comments WHERE comment_ID IN (20,19,18,17,16,15,14,12,10,9,7,6,5,4,3,2,1",
            ")"
        ],
        [
            "SELECT COUNT( 1 ) FROM wp_posts WHERE post_type = 'post' AND post_status NOT IN ('trash', 'auto-draft') AND ID IN (35",
            ")"
        ],
        [
            "SELECT comment_id, meta_key, meta_value FROM wp_commentmeta WHERE comment_id IN (1,2,3,4,5,6,7,9,10,12,14,15,16,17,18,19,20",
            ") ORDER BY meta_id ASC"
        ],
        [
            "SELECT post_author, COUNT(*) FROM wp_posts WHERE ( ( post_type = 'post' AND ( post_status = 'publish' OR post_status = 'private' ) ) ) AND post_author IN (1",
            ") GROUP BY post_author"
        ],
        [
            "SELECT wp_comments.comment_ID FROM wp_comments WHERE ( ( comment_approved = '1' ) OR ( user_id = 1 AND comment_approved = '0' ) ) AND comment_post_ID = 1 AND comment_parent IN ( 1",
            " ) ORDER BY wp_comments.comment_date_gmt ASC, wp_comments.comment_ID ASC "
        ],
        [
            "SELECT wp_posts.ID FROM wp_posts LEFT JOIN wp_postmeta ON ( wp_posts.ID = wp_postmeta.post_id AND wp_postmeta.meta_key = '_customize_restore_dismissed' ) WHERE 1=1 AND wp_posts.post_author IN (1",
            ") AND ( wp_postmeta.post_id IS NULL ) AND wp_posts.post_type = 'customize_changeset' AND ((wp_posts.post_status = 'auto-draft')) GROUP BY wp_posts.ID ORDER BY wp_posts.post_date DESC LIMIT 0, 1"
        ],
        [
            "SELECT wp_comments.comment_ID FROM wp_comments WHERE ( ( comment_approved = '1' ) OR ( user_id = 1 AND comment_approved = '0' ) ) AND comment_post_ID = 1 AND comment_parent IN ( 1,2",
            " ) ORDER BY wp_comments.comment_date_gmt ASC, wp_comments.comment_ID ASC"
        ],
        [
            "SELECT t.*, tt.*, tr.object_id FROM wp_terms AS t INNER JOIN wp_term_taxonomy AS tt ON t.term_id = tt.term_id INNER JOIN wp_term_relationships AS tr ON tr.term_taxonomy_id = tt.term_taxonomy_id WHERE tt.taxonomy IN ('category', 'post_tag', 'post_format') AND tr.object_id IN (1",
            ") ORDER BY t.name ASC"
        ],
    ],
    "num_2_parenthesis": [
        [
            "SELECT SQL_CALC_FOUND_ROWS wp_posts.ID FROM wp_posts LEFT JOIN wp_term_relationships ON (wp_posts.ID = wp_term_relationships.object_id) WHERE 1=1 AND ( wp_term_relationships.term_taxonomy_id IN (1",
            ") ) AND wp_posts.post_type = 'post' AND ((wp_posts.post_status = 'trash')) GROUP BY wp_posts.ID ORDER BY wp_posts.post_date DESC LIMIT 0, 20"
        ],
        [
            "SELECT SQL_CALC_FOUND_ROWS wp_posts.ID FROM wp_posts LEFT JOIN wp_term_relationships ON (wp_posts.ID = wp_term_relationships.object_id) WHERE 1=1 AND YEAR(wp_posts.post_date)=2021 AND MONTH(wp_posts.post_date)=12 AND ( wp_term_relationships.term_taxonomy_id IN (2",
            ") ) AND wp_posts.post_type = 'post' AND ((wp_posts.post_status = 'trash')) GROUP BY wp_posts.ID ORDER BY wp_posts.post_date DESC LIMIT 0, 20"
        ]
    ],
}