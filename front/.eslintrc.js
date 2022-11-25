module.exports = {
  'env': {
    'browser': true,
    'es2021': true,
    'node': true
  },
  'extends': [
    'eslint:recommended',
    'plugin:react/recommended'
  ],
  'parserOptions': {
    'ecmaFeatures': {
      'jsx': true
    },
    'ecmaVersion': 'latest',
    'sourceType': 'module'
  },
  'plugins': [
    'react'
  ],
  'rules': {
    'indent': ['warn', 2],
    'no-trailing-spaces': 'warn',
    'semi': 'warn',
    'quotes': ['warn', 'single'],
    'no-unused-vars': 'warn',
    'react/prop-types': 'off',
  }
};
