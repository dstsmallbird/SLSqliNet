<?php
/**
 * The base configuration for WordPress
 *
 * The wp-config.php creation script uses this file during the installation.
 * You don't have to use the web site, you can copy this file to "wp-config.php"
 * and fill in the values.
 *
 * This file contains the following configurations:
 *
 * * MySQL settings
 * * Secret keys
 * * Database table prefix
 * * ABSPATH
 *
 * @link https://wordpress.org/support/article/editing-wp-config-php/
 *
 * @package WordPress
 */

// ** MySQL settings - You can get this info from your web host ** //
/** The name of the database for WordPress */
define( 'DB_NAME', 'wordpress' );

/** MySQL database username */
define( 'DB_USER', 'wp' );

/** MySQL database password */
define( 'DB_PASSWORD', 'Huang.399' );

/** MySQL hostname */
define( 'DB_HOST', 'localhost' );

/** Database charset to use in creating database tables. */
define( 'DB_CHARSET', 'utf8' );

/** The database collate type. Don't change this if in doubt. */
define( 'DB_COLLATE', '' );

/**#@+
 * Authentication unique keys and salts.
 *
 * Change these to different unique phrases! You can generate these using
 * the {@link https://api.wordpress.org/secret-key/1.1/salt/ WordPress.org secret-key service}.
 *
 * You can change these at any point in time to invalidate all existing cookies.
 * This will force all users to have to log in again.
 *
 * @since 2.6.0
 */
define( 'AUTH_KEY',         'X)+nV4;{2E6)i4 S`}c XCi K[U`Xriy,C6H+=U}$Wo.@jI4Q|cpOyG4+C(DTLI+' );
define( 'SECURE_AUTH_KEY',  'z*e7;l5nu|oo@)_t&[5qWh%{&2X,KwWU.^yn1*pm{.#.lK3MqM_T?w|i5aNPUR1j' );
define( 'LOGGED_IN_KEY',    '!r@6]wM5n;G}|m#oHQy,yZ_6uH{P[9 )|Ftrj;|/Y|s;zOMu:;F[TvF|[S<ZYb#S' );
define( 'NONCE_KEY',        'B9L,V:lq|bb5U?Oi/yaFV#hoEdVI&|$P2RPR)`8bGMq_I+Ad_:vBCC@-+[$&YDA)' );
define( 'AUTH_SALT',        'p=u080UjuHF{Sz?<}l%-V1iU>e;E[(lU4{s<JkH _by =E`6]+5k@p%9{SPhWHA%' );
define( 'SECURE_AUTH_SALT', 'UH8N{<=-%|/..X&PQTl Dl>tEu`-&itT%,-7?.&s7.uOq.X(IYr~u953&!!Jqy|,' );
define( 'LOGGED_IN_SALT',   '<y$pQq]Av3o::0)QZC+B$WydV>M(uh-[V*J;znw7SUUPa,4&fj5}k<i{~]-T$S~c' );
define( 'NONCE_SALT',       '}-!+A*vN-HE{niTFw9Xng&A)0J)Hq!ueyYStCi+/HD:3]Y}yg) &v;ds*b<1vJWr' );

/**#@-*/

/**
 * WordPress database table prefix.
 *
 * You can have multiple installations in one database if you give each
 * a unique prefix. Only numbers, letters, and underscores please!
 */
$table_prefix = 'wp_';

/**
 * For developers: WordPress debugging mode.
 *
 * Change this to true to enable the display of notices during development.
 * It is strongly recommended that plugin and theme developers use WP_DEBUG
 * in their development environments.
 *
 * For information on other constants that can be used for debugging,
 * visit the documentation.
 *
 * @link https://wordpress.org/support/article/debugging-in-wordpress/
 */
define( 'WP_DEBUG', false );

/* Add any custom values between this line and the "stop editing" line. */



/* That's all, stop editing! Happy publishing. */

/** Absolute path to the WordPress directory. */
if ( ! defined( 'ABSPATH' ) ) {
	define( 'ABSPATH', __DIR__ . '/' );
}

/** Sets up WordPress vars and included files. */
require_once ABSPATH . 'wp-settings.php';
