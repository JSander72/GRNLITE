const path = require('path');

module.exports = {
  entry: {
    auth: './staticfiles/JS/auth.js',
    file: './staticfiles/JS/file.js',
    signup: './staticfiles/JS/signup.js',
  },
  output: {
    filename: '[name].bundle.js',
    path: path.resolve(__dirname, '../dist'),
  },
  module: {
    rules: [
      {
        test: /\.js$/,
        exclude: /node_modules/,
        use: {
          loader: 'babel-loader',
        },
      },
    ],
  },
  externals: {
    pg: 'commonjs pg', 
  },
  mode: 'development',
  target: 'web',
};