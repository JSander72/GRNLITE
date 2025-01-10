'use strict';

import fs from 'fs';
import path from 'path';
import browserify from 'browserify';
import uglify from 'uglify-js';

const pkg = process.argv[2];
const standalone = process.argv[3];
const compress = process.argv[4];

let packageDir = path.join(__dirname, '..');
if (pkg !== '.') packageDir = path.join(packageDir, 'node_modules', pkg);

const json = require(path.join(packageDir, 'package.json'));

const distDir = path.join(__dirname, '..', 'dist');
if (!fs.existsSync(distDir)) fs.mkdirSync(distDir);

const bOpts = {};
if (standalone) bOpts.standalone = standalone;

browserify(bOpts)
.require(path.join(packageDir, json.main), {expose: json.name})
.bundle(function (err, buf) {
  if (err) {
    console.error('browserify error:', err);
    process.exit(1);
  }

  const outputFile = path.join(distDir, json.name);
  const uglifyOpts = {
    warnings: true,
    compress: {},
    output: {
      preamble: '/* ' + json.name + ' ' + json.version + ': ' + json.description + ' */'
    }
  };
  if (compress) {
    const compressOpts = compress.split(',');
    for (let i=0, il = compressOpts.length; i<il; ++i) {
      const pair = compressOpts[i].split('=');
      uglifyOpts.compress[pair[0]] = pair.length < 1 || pair[1] !== 'false';
    }
  }
  if (standalone) {
    uglifyOpts.sourceMap = {
      filename: json.name + '.min.js',
      url: json.name + '.min.js.map'
    };
  }

  const result = uglify.minify(buf.toString(), uglifyOpts);
  fs.writeFileSync(outputFile + '.min.js', result.code);
  if (result.map) fs.writeFileSync(outputFile + '.min.js.map', result.map);
  if (standalone) fs.writeFileSync(outputFile + '.bundle.js', buf);
  if (result.warnings) {
    for (let j=0, jl = result.warnings.length; j<jl; ++j)
      console.warn('UglifyJS warning:', result.warnings[j]);
  }
});
