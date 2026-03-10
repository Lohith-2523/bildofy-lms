import { format, parseISO, isValid } from "date-fns";

type DateInput = Date | string | null | undefined;

const toDate = (value: DateInput): Date | null => {
  if (!value) return null;
  if (value instanceof Date) {
    return isValid(value) ? value : null;
  }

  const parsed = parseISO(value);
  if (isValid(parsed)) {
    return parsed;
  }

  const fallback = new Date(value);
  return isValid(fallback) ? fallback : null;
};

export const formatDisplayDate = (value: DateInput): string => {
  const date = toDate(value);
  return date ? format(date, "dd-MM-yyyy") : "-";
};
