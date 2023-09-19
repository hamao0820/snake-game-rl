const path = require('path');
const HtmlWebpackPlugin = require('html-webpack-plugin');

module.exports = {
    entry: {
        main: './src/ts/index.ts',
    },

    output: {
        path: path.join(__dirname, 'dist'),
    },

    resolve: {
        extensions: ['.ts', '.js'],
    },

    module: {
        rules: [
            {
                test: /\.ts$/,
                loader: 'ts-loader',
            },
            {
                test: /\.css/,
                use: [
                    'style-loader',
                    {
                        loader: 'css-loader',
                        options: { url: false },
                    },
                ],
            },
        ],
    },

    plugins: [
        new HtmlWebpackPlugin({
            //	追加
            inject: 'body',
            filename: 'index.html',
            template: './src/index.html',
            chunks: ['index'],
        }),
    ],
};
