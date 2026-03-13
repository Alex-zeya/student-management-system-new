// ModalForm Component - Unified Style
// Usage: <ModalForm title="Title" onClose={() => setOpen(false)} onSubmit={handleSubmit} submitting={saving} submitText="Save">
//   ...form fields
// </ModalForm>

import React from 'react';

interface ModalFormProps {
  title: string;
  subtitle?: string;
  icon?: React.ReactNode;
  onClose: () => void;
  onSubmit: () => void;
  submitting: boolean;
  submitText?: string;
  children: React.ReactNode;
  error?: string;
  size?: 'sm' | 'md' | 'lg' | 'xl';
  theme?: 'green' | 'gray' | 'blue' | 'purple';
}

const themeColors = {
  green: {
    gradient: 'from-white to-gray-50',
    ring: 'focus:ring-green-500',
    bg: 'bg-white',
    text: 'text-gray-900',
    border: 'border-gray-200',
    hover: 'hover:bg-gray-50',
  },
  gray: {
    gradient: 'from-white to-gray-50',
    ring: 'focus:ring-gray-500',
    bg: 'bg-white',
    text: 'text-gray-900',
    border: 'border-gray-200',
    hover: 'hover:bg-gray-50',
  },
  blue: {
    gradient: 'from-white to-gray-50',
    ring: 'focus:ring-blue-500',
    bg: 'bg-white',
    text: 'text-gray-900',
    border: 'border-gray-200',
    hover: 'hover:bg-gray-50',
  },
  purple: {
    gradient: 'from-white to-gray-50',
    ring: 'focus:ring-purple-500',
    bg: 'bg-white',
    text: 'text-gray-900',
    border: 'border-gray-200',
    hover: 'hover:bg-gray-50',
  },
};

const sizeWidth = {
  sm: 'max-w-md',
  md: 'max-w-lg',
  lg: 'max-w-2xl',
  xl: 'max-w-4xl',
};

export const ModalForm: React.FC<ModalFormProps> = ({
  title,
  subtitle,
  icon,
  onClose,
  onSubmit,
  submitting,
  submitText = 'Save',
  children,
  error,
  size = 'md',
  theme = 'green',
}) => {
  const colors = themeColors[theme];

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4">
      {/* Background overlay */}
      <div 
        className="absolute inset-0 bg-gradient-to-br from-gray-900/60 via-gray-800/50 to-gray-900/60 backdrop-blur-md"
        onClick={(e) => {
          // Only close when clicking the overlay itself (not the modal content)
          if (e.target === e.currentTarget) {
            onClose();
          }
        }}
      />
      
      {/* Modal body */}
      <div className={`relative w-full ${sizeWidth[size]} transform transition-all duration-300 ease-out`}>
        <div className="bg-white/95 backdrop-blur-xl rounded-3xl shadow-2xl border border-white/20 overflow-hidden">
          {/* Top decorative bar */}
          <div className={`h-1.5 bg-gradient-to-r from-green-500 to-emerald-600`} />
          
          {/* Header */}
          <div className="px-8 pt-8 pb-4">
            <div className="flex items-start gap-4">
              {icon && (
                <div className="w-12 h-12 rounded-2xl bg-gradient-to-r from-green-500 to-emerald-600 flex items-center justify-center text-white shadow-lg shadow-green-500/30">
                  {icon}
                </div>
              )}
              <div className="flex-1">
                <h3 className="text-2xl font-bold text-gray-900">{title}</h3>
                {subtitle && <p className="text-sm text-gray-500 mt-1">{subtitle}</p>}
              </div>
              <button
                onClick={onClose}
                className="w-10 h-10 rounded-xl bg-gray-100 hover:bg-gray-200 flex items-center justify-center text-gray-400 hover:text-gray-600 transition-all"
              >
                <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>
          </div>
          
          {/* Error message */}
          {error && (
            <div className="mx-8 mb-4">
              <div className="flex items-center gap-3 px-4 py-3 bg-red-50 border border-red-100 rounded-2xl">
                <svg className="w-5 h-5 text-red-500 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                <p className="text-sm text-red-600">{error}</p>
              </div>
            </div>
          )}
          
          {/* Content area */}
          <div className="px-8 pb-8 max-h-[75vh] overflow-y-auto">
            {children}
          </div>
          
          {/* Footer buttons */}
          <div className="px-8 py-6 bg-gray-50/80 border-t border-gray-100 flex justify-end gap-3">
            <button
              onClick={onClose}
              className="px-6 py-3 text-sm font-medium text-gray-600 hover:text-gray-800 hover:bg-gray-100 rounded-xl transition-all"
            >
              cancel
            </button>
            <button
              onClick={onSubmit}
              disabled={submitting}
              className="px-8 py-3 bg-white border-2 border-gray-200 text-gray-900 text-sm font-medium rounded-xl hover:bg-gray-50 hover:border-gray-300 disabled:opacity-50 disabled:cursor-not-allowed transition-all flex items-center gap-2 shadow-sm"
            >
              {submitting && (
                <svg className="w-4 h-4 animate-spin" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
                </svg>
              )}
              {submitText}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

// Input component
interface InputFieldProps {
  label: string;
  value: string;
  onChange: (value: string) => void;
  placeholder?: string;
  required?: boolean;
  type?: 'text' | 'email' | 'password' | 'number' | 'datetime-local';
  icon?: React.ReactNode;
  error?: string;
  rows?: number;
  multiline?: boolean;
}

export const InputField: React.FC<InputFieldProps> = ({
  label,
  value,
  onChange,
  placeholder,
  required,
  type = 'text',
  icon,
  error,
  rows = 1,
  multiline = false,
}) => {
  const inputClasses = `
    w-full px-4 py-3.5 text-gray-900 placeholder-gray-400 
    bg-gray-50 border-2 border-gray-100 rounded-2xl
    focus:bg-white focus:border-green-500 focus:ring-4 focus:ring-green-500/10
    transition-all duration-200
    ${icon ? 'pl-12' : ''}
    ${error ? 'border-red-300 focus:border-red-500 focus:ring-red-500/10' : ''}
  `;

  return (
    <div className="space-y-2">
      <label className="flex items-center gap-2 text-sm font-semibold text-gray-700">
        {icon && <span className="text-gray-400">{icon}</span>}
        {label}
        {required && <span className="text-red-500">*</span>}
      </label>
      {multiline ? (
        <textarea
          value={value}
          onChange={e => onChange(e.target.value)}
          placeholder={placeholder}
          rows={rows}
          className={`${inputClasses} resize-none`}
        />
      ) : (
        <input
          type={type}
          value={value}
          onChange={e => onChange(e.target.value)}
          placeholder={placeholder}
          className={inputClasses}
        />
      )}
      {error && <p className="text-xs text-red-500 mt-1">{error}</p>}
    </div>
  );
};

// Select component
interface SelectFieldProps {
  label: string;
  value: string | number;
  onChange: (value: string | number) => void;
  options: { value: string | number; label: string }[];
  placeholder?: string;
  required?: boolean;
  icon?: React.ReactNode;
}

export const SelectField: React.FC<SelectFieldProps> = ({
  label,
  value,
  onChange,
  options,
  placeholder,
  required,
  icon,
}) => {
  return (
    <div className="space-y-2">
      <label className="flex items-center gap-2 text-sm font-semibold text-gray-700">
        {icon && <span className="text-gray-400">{icon}</span>}
        {label}
        {required && <span className="text-red-500">*</span>}
      </label>
      <div className="relative">
        <select
          value={value}
          onChange={e => onChange(e.target.value ? (e.target.value === '' ? '' : Number(e.target.value) || e.target.value) : '')}
          className={`
            w-full px-4 py-3.5 text-gray-900
            bg-gray-50 border-2 border-gray-100 rounded-2xl
            focus:bg-white focus:border-green-500 focus:ring-4 focus:ring-green-500/10
            transition-all duration-200 appearance-none cursor-pointer
            ${icon ? 'pl-12' : ''}
          `}
        >
          {placeholder && <option value="">{placeholder}</option>}
          {options.map(opt => (
            <option key={opt.value} value={opt.value}>{opt.label}</option>
          ))}
        </select>
        <div className="absolute right-4 top-1/2 -translate-y-1/2 pointer-events-none">
          <svg className="w-5 h-5 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
          </svg>
        </div>
      </div>
    </div>
  );
};

// Checkbox component
interface CheckboxFieldProps {
  label: string;
  checked: boolean;
  onChange: (checked: boolean) => void;
}

export const CheckboxField: React.FC<CheckboxFieldProps> = ({
  label,
  checked,
  onChange,
}) => {
  return (
    <label className="flex items-center gap-3 cursor-pointer group">
      <div className="relative">
        <input
          type="checkbox"
          checked={checked}
          onChange={e => onChange(e.target.checked)}
          className="sr-only"
        />
        <div 
          className={`
            w-6 h-6 rounded-lg border-2 flex items-center justify-center transition-all duration-200
            ${checked 
              ? 'bg-green-500 border-green-500' 
              : 'bg-white border-gray-300 group-hover:border-green-400'
            }
          `}
        >
          {checked && (
            <svg className="w-4 h-4 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={3} d="M5 13l4 4L19 7" />
            </svg>
          )}
        </div>
      </div>
      <span className="text-sm font-medium text-gray-700 group-hover:text-gray-900 transition-colors">
        {label}
      </span>
    </label>
  );
};

// File upload component
interface FileFieldProps {
  label: string;
  value: File | null;
  onChange: (file: File | null) => void;
  accept?: string;
  required?: boolean;
}

export const FileField: React.FC<FileFieldProps> = ({
  label,
  value,
  onChange,
  accept,
  required,
}) => {
  return (
    <div className="space-y-2">
      <label className="text-sm font-semibold text-gray-700">
        {label}
        {required && <span className="text-red-500">*</span>}
      </label>
      <div className={`
        relative border-2 border-dashed rounded-2xl p-6
        ${value ? 'border-green-300 bg-green-50' : 'border-gray-200 hover:border-green-400 hover:bg-gray-50'}
        transition-all duration-200 cursor-pointer
      `}>
        <input
          type="file"
          accept={accept}
          onChange={e => onChange(e.target.files?.[0] ?? null)}
          className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
        />
        <div className="flex flex-col items-center gap-2">
          {value ? (
            <>
              <div className="w-12 h-12 rounded-xl bg-green-100 flex items-center justify-center">
                <svg className="w-6 h-6 text-green-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <p className="text-sm font-medium text-gray-900">{value.name}</p>
              <p className="text-xs text-gray-500">Click to change file</p>
            </>
          ) : (
            <>
              <div className="w-12 h-12 rounded-xl bg-gray-100 flex items-center justify-center">
                <svg className="w-6 h-6 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
                </svg>
              </div>
              <p className="text-sm font-medium text-gray-600">Click to upload file</p>
              <p className="text-xs text-gray-400">Supports PDF, Word, Image formats</p>
            </>
          )}
        </div>
      </div>
    </div>
  );
};

export default { ModalForm, InputField, SelectField, CheckboxField, FileField };
