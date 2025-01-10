
import { fileURLToPath } from 'url';
import path from 'path';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
export default {
  entry: {
    auth: './staticfiles/JS/auth.js',
    file: './staticfiles/JS/file.js',
    signup: './staticfiles/JS/signup.js',
  },
  output: {
    filename: '[name].bundle.js',
    path: path.resolve(__dirname, 'dist'),
  },
  plugins: [
    new CopyWebpackPlugin({
      patterns: [
        {
          from: path.resolve(__dirname, 'staticfiles/JS'),
          to: path.resolve(__dirname, 'dist/js'),
        },
      ],
    }),
  ],
};