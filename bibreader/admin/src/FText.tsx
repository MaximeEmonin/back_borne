import { TextField } from "@mui/material";
import { useController, useFormContext } from "react-hook-form";

const FText = ({ name, label }: { name: string; label: string }) => {
  const { control } = useFormContext();

  const {
    field: { value, onChange, ref },
    fieldState: { error },
  } = useController({
    name,
    control,
  });

  return (
    <TextField
      error={Boolean(error)}
      helperText={error?.message}
      value={value}
      onChange={onChange}
      inputRef={ref}
      label={label}
    />
  );
};

export default FText;
