import { ComponentFixture, TestBed } from '@angular/core/testing';

import { UploadCobrosViewComponent } from './upload-cobros-view.component';

describe('UploadCobrosViewComponent', () => {
  let component: UploadCobrosViewComponent;
  let fixture: ComponentFixture<UploadCobrosViewComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [UploadCobrosViewComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(UploadCobrosViewComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
