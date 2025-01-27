import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ChangeProveedorViewComponent } from './change-proveedor-view.component';

describe('ChangeProveedorViewComponent', () => {
  let component: ChangeProveedorViewComponent;
  let fixture: ComponentFixture<ChangeProveedorViewComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ChangeProveedorViewComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(ChangeProveedorViewComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
