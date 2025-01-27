import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CreateProcesosViewComponent } from './create-procesos-view.component';

describe('CreateProcesosViewComponent', () => {
  let component: CreateProcesosViewComponent;
  let fixture: ComponentFixture<CreateProcesosViewComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [CreateProcesosViewComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(CreateProcesosViewComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
