# JioPulse Attendance Handbook

## Minimum attendance rule
Students are expected to maintain at least **75% attendance** in every
subject. Anyone below 75% is considered "short of attendance" and may be
flagged for review. A student between 65% and 75% is "at risk" and should be
warned early. Below 65% is "critical".

## How face attendance works
A teacher opens a subject, adds one or more classroom photos, and runs the
face analysis. JioPulse detects every enrolled student's face from the photos
using facial embeddings and marks them present in a single pass. Students who
are enrolled but not detected in any photo are marked absent for that session.

## How voice attendance works
In voice mode students say a short phrase one by one (for example, "I am
present"). JioPulse compares each recording against the student's stored voice
signature and marks the closest match present. Voice is useful when a clear
group photo is hard to capture.

## Enrolling in a subject
Every subject has a unique join code and QR code. A student scans the QR code
or opens the share link, which auto-enrolls them into that subject. Teachers
can share the code from the "Manage Subjects" screen.

## Biometric privacy
Face and voice data are stored only as mathematical embeddings, never as raw
photos or recordings the system replays. Embeddings are used solely to match
attendance and are tied to the student's own profile.

## Reading attendance records
The teacher dashboard groups attendance by session and shows how many students
were present out of the total for each class. Students see their own
percentage per subject on their dashboard.

## Improving low attendance
To raise a percentage, a student must attend upcoming sessions. Because the
percentage is present-sessions divided by total-sessions, missed classes
cannot be edited away; only future attendance moves the number.
