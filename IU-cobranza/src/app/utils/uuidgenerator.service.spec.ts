import { TestBed } from '@angular/core/testing';

import { UuidgeneratorService } from './uuidgenerator.service';

describe('UuidgeneratorService', () => {
  let service: UuidgeneratorService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(UuidgeneratorService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
