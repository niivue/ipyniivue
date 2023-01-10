// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.

// Add any needed widget imports here (or from controls)
// import {} from '@jupyter-widgets/base';

import { createTestModel } from './utils';

import { NiivueModel } from '..';

describe('NiiVue', () => {
  describe('NiivueModel', () => {
    it('should be createable', () => {
      const model = createTestModel(NiivueModel);
      expect(model).toBeInstanceOf(NiivueModel);
      expect(model.get('height')).toEqual(480);
    });

    it('should be createable with a value', () => {
      const state = { height: 600 };
      const model = createTestModel(NiivueModel, state);
      expect(model).toBeInstanceOf(NiivueModel);
      expect(model.get('height')).toEqual(600);
    });
  });
});
