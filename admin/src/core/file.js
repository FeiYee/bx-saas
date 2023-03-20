
export const getFileType = (fileType) => {
  switch (fileType) {
    case 0:
      return 'Image'
    case 1:
      return 'Excel'
    case 2:
      return 'PDF'
    case 3:
      return 'ZIP'
    default:
      return 'Other'
  }
}
