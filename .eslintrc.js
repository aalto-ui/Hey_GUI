module.exports = {
  'env': {
    'browser': true,
    'es6': true,
  },
  'extends': [
    'google',
  ],
  'globals': {
    'Atomics': 'readonly',
    'SharedArrayBuffer': 'readonly',
  },
  'parserOptions': {
    'ecmaVersion': 2018,
  },
  'rules': {
    'indent': ['error', 4],
    'max-len': 0,
    'no-var': 0,
    'require-jsdoc': 0,
    'no-unused-vars': 1,
  },
};
