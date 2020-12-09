module.exports = {
  env: {
    browser: true,
    es2021: true
  },
  extends: ['airbnb'],
  parserOptions: {
    ecmaFeatures: {
      jsx: true
    },
    ecmaVersion: 12,
    sourceType: 'module'
  },
  plugins: ['react'],
  rules: {
    'import/prefer-default-export': 'off',
    quotes: ['error', 'double'],
    'linebreak-style': ['error', 'unix'],
    'react/prop-types': [0],
  }
};
