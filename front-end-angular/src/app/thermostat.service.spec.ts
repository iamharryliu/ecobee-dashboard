import { TestBed } from '@angular/core/testing';

import { ThermostatService } from './thermostat.service';

describe('ThermostatService', () => {
  beforeEach(() => TestBed.configureTestingModule({}));

  it('should be created', () => {
    const service: ThermostatService = TestBed.get(ThermostatService);
    expect(service).toBeTruthy();
  });
});
