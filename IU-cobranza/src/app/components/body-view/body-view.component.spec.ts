import { ComponentFixture, TestBed } from '@angular/core/testing';

import { BodyViewComponent } from './body-view.component';

describe('BodyViewComponent', () => {
  let component: BodyViewComponent;
  let fixture: ComponentFixture<BodyViewComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [BodyViewComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(BodyViewComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
