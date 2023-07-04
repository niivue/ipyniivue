module.exports = {
  automock: false,
  moduleNameMapper: {
    '\\.(css|less|sass|scss)$': 'identity-obj-proxy',
    "\\.(jpg|jpeg|png|gif)$": "<rootDir>/fileMock.js",
  },
  preset: 'ts-jest/presets/js-with-babel',
  moduleFileExtensions: ['ts', 'tsx', 'js', 'jsx', 'json', 'node'],
  testPathIgnorePatterns: ['/lib/', '/node_modules/'],
  testRegex: '/__tests__/.*.spec.ts[x]?$',
  transformIgnorePatterns: [
    '/node_modules/(?!(@jupyter(lab|-widgets)|@niivue)/.*)',
  ],
  transform: {
    "^.+\\.(ts|tsx|js|jsx)?$": "babel-jest"
  },
  globals: {
    'ts-jest': {
      tsconfig: '<rootDir>/tsconfig.json',
    },
  },
};
