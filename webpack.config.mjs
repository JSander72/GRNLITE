import CopyWebpackPlugin from 'copy-webpack-plugin';
import { fileURLToPath } from 'url';
import path from 'path';
import fs from 'fs';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const copyFiles = () => {
  const sourceDir = path.resolve(__dirname, 'staticfiles/JS');
  const targetDir = path.resolve(__dirname, 'dist/js');
  fs.mkdirSync(targetDir, { recursive: true });
  fs.readdirSync(sourceDir).forEach(file => {
    fs.copyFileSync(path.join(sourceDir, file), path.join(targetDir, file));
  });
};

copyFiles();

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
