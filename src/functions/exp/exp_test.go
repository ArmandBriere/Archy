package exp_test

import (
	"reflect"
	"testing"
	"time"

	exp "exp.com/cloudfunction"
)

func TestVerifyTimestamp(t *testing.T) {
	tests := []struct {
		text string
		in   string
		want bool
	}{
		{
			text: "Now",
			in:   time.Now().UTC().Format(exp.DATETIME_FORMAT_EXAMPLE),
			want: false,
		},
		{
			text: "30 sec ago",
			in:   time.Now().Add(-time.Second * 30).UTC().Format(exp.DATETIME_FORMAT_EXAMPLE),
			want: false,
		},
		{
			text: "59 sec ago",
			in:   time.Now().Add(-time.Second * 59).UTC().Format(exp.DATETIME_FORMAT_EXAMPLE),
			want: false,
		},
		{
			text: "60 sec ago",
			in:   time.Now().Add(-time.Second * 60).UTC().Format(exp.DATETIME_FORMAT_EXAMPLE),
			want: true,
		},
		{
			text: "61 sec ago",
			in:   time.Now().Add(-time.Second * 61).UTC().Format(exp.DATETIME_FORMAT_EXAMPLE),
			want: true,
		},
	}

	for _, tt := range tests {
		got := exp.ExportVerifyTimestamp(tt.in)

		if !reflect.DeepEqual(got, tt.want) {
			t.Errorf("exp.verifyTimestamp(%s)=%#v; want %v", tt.text, got, tt.want)
		}
	}
}

// Test that the user level match total exp.
func TestGetUserLevel(t *testing.T) {

	tests := []struct {
		in   int
		want []int
	}{
		{
			in:   0,
			want: []int{0, 100},
		},
		{
			in:   100,
			want: []int{1, 155},
		},
		{
			in:   10044,
			want: []int{13, 1},
		},
		{
			in:   10045,
			want: []int{14, 1780},
		},
		{
			in:   46474,
			want: []int{25, 1},
		},
		{
			in:   46475,
			want: []int{26, 4780},
		},
		{
			in:   283475,
			want: []int{51, 15655},
		},
		{
			in:   660000,
			want: []int{69, 27225},
		},
	}

	for _, tt := range tests {
		t.Run("", func(t *testing.T) {
			first, second := exp.ExportGetUserLevel(tt.in)

			if !reflect.DeepEqual(first, tt.want[0]) {
				t.Errorf("exp.getUserLevel(%d)=%#v; want %v", tt.in, first, tt.want[0])
			}
			if !reflect.DeepEqual(second, tt.want[1]) {
				t.Errorf("exp.getUserLevel(%d)=%#v; want %v", tt.in, second, tt.want[1])
			}
		})
	}
}
