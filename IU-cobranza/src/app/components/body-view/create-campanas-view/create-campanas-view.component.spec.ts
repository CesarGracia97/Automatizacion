import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CreateCampanasViewComponent } from './create-campanas-view.component';

describe('CreateCampanasViewComponent', () => {
  let component: CreateCampanasViewComponent;
  let fixture: ComponentFixture<CreateCampanasViewComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [CreateCampanasViewComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(CreateCampanasViewComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
