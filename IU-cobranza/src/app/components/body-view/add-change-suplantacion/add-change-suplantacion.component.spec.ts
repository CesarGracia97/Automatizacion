import { ComponentFixture, TestBed } from '@angular/core/testing';

import { AddChangeSuplantacionComponent } from './add-change-suplantacion.component';

describe('AddChangeSuplantacionComponent', () => {
  let component: AddChangeSuplantacionComponent;
  let fixture: ComponentFixture<AddChangeSuplantacionComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [AddChangeSuplantacionComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(AddChangeSuplantacionComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
