import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@zcode/ui/select";

const EMPTY_OPTION = "__education_empty_option__";

export function EducationSelect({
  label,
  value,
  onValueChange,
  options,
  disabled,
  className,
}: {
  label: string;
  value: string;
  onValueChange: (value: string) => void;
  options: readonly { value: string; label: string }[];
  disabled?: boolean;
  className?: string;
}) {
  // Radix 的空值代表清空选择；学科“全部”是有效领域值，因此在展示边界编码。
  const hasEmptyOption = options.some((option) => option.value === "");
  return (
    <Select
      value={value === "" && hasEmptyOption ? EMPTY_OPTION : value}
      disabled={disabled}
      onValueChange={(next) => onValueChange(next === EMPTY_OPTION ? "" : next)}
    >
      <SelectTrigger aria-label={label} size="lg" variant="input" className={className}>
        <SelectValue placeholder="请选择" />
      </SelectTrigger>
      <SelectContent position="popper">
        {options.map((option) => (
          <SelectItem key={option.value} value={option.value || EMPTY_OPTION}>
            {option.label}
          </SelectItem>
        ))}
      </SelectContent>
    </Select>
  );
}
