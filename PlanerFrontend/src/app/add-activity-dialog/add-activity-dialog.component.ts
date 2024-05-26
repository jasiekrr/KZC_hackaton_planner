import { Component, Inject } from '@angular/core';
import { MatDialogRef, MAT_DIALOG_DATA } from '@angular/material/dialog';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';

@Component({
  selector: 'app-add-activity-dialog',
  templateUrl: './add-activity-dialog.component.html',
  styleUrls: ['./add-activity-dialog.component.css'],
})
export class AddActivityDialogComponent {
  activityForm: FormGroup;
  subjects: string[];
  teachers: string[];
  formats: string[];
  types: string[];

  constructor(
    public dialogRef: MatDialogRef<AddActivityDialogComponent>,
    private fb: FormBuilder,
    @Inject(MAT_DIALOG_DATA) public data: any
  ) {
    this.subjects = data.subjects;
    this.teachers = data.teachers;
    this.formats = data.formats;
    this.types = data.types;

    this.activityForm = this.fb.group({
      subjectName: ['', Validators.required],
      mainTeacher: ['', Validators.required],
      format: ['', Validators.required],
      type: ['', Validators.required],
      deadline: ['', Validators.required],
      multiplier: [1, Validators.required]
    });
  }

  onSubmit(): void {
    if (this.activityForm.valid) {
      this.dialogRef.close(this.activityForm.value);
    }
  }

  onCancel(): void {
    this.dialogRef.close();
  }
}
